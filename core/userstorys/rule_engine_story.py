import uuid
from datetime import datetime
from typing import List, Optional
import time

from core.interfaces.userstorys.rule_engine_story import IRuleEngineStory
from core.interfaces.database.unit_of_work import IUnitOfWork
from core.models.rule_engine import (
    RiskAssessmentResult, RuleConfig, RuleResult, 
    RuleType, RiskLevel
)
from core.models.data_base.mongo_models import VerificationLogModel
from core.models.data_base.onbaording_models import VerificationRequestModel
from core.infra.mongodb.mongo_base_repository import MongoBaseRepository
from core.infra.postgresql.postgres_base_repository import PostgresBaseRepository

class RuleEngineStory(IRuleEngineStory):
    def __init__(self, uow_postgres: IUnitOfWork, uow_mongo: IUnitOfWork):
        self._uow_postgres = uow_postgres
        self._uow_mongo = uow_mongo
        self._default_config = RuleConfig()

    async def assess_risk(self, verification_data, config: Optional[RuleConfig] = None) -> RiskAssessmentResult:
        """
        Evalúa el riesgo de una solicitud de verificación aplicando las reglas configuradas.
        
        Args:
            verification_data: Datos de la verificación (debe tener email, country_id, document_number)
            config: Configuración de reglas (opcional)
        
        Returns:
            RiskAssessmentResult: Resultado de la evaluación de riesgo
        """
        start_time = time.time()
        rule_config = config or self._default_config
        
        # Aplicar todas las reglas
        rules_results = [
            self._check_email_domain(verification_data, rule_config),
            self._check_country_restricted(verification_data, rule_config),
            self._check_document_length(verification_data, rule_config)
        ]
        
        # Calcular score (100 puntos iniciales, restar penalizaciones)
        initial_score = 100
        total_penalty = sum(rule.score_penalty for rule in rules_results if rule.triggered)
        final_score = max(0, initial_score - total_penalty)
        
        # Determinar nivel de riesgo
        risk_level = self._determine_risk_level(final_score)
        
        # Preparar detalles de reglas activadas
        triggered_rules = [rule.rule_type for rule in rules_results if rule.triggered]
        rules_detail = {
            rule.rule_type: rule.details 
            for rule in rules_results 
            if rule.triggered
        }
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return RiskAssessmentResult(
            score=final_score,
            risk_level=risk_level,
            rules_triggered=triggered_rules,
            rules_detail=rules_detail,
            processing_time_ms=processing_time_ms
        )

    async def process_pending_verifications(self, batch_size: int = 100) -> dict:
        """
        Procesa todas las verificaciones pendientes aplicando el motor de reglas.
        
        Args:
            batch_size: Tamaño del lote para procesamiento
            
        Returns:
            dict: Estadísticas del procesamiento
        """
        stats = {
            "processed": 0,
            "updated": 0,
            "errors": 0
        }

        async with self._uow_postgres as uow_postgres:
            try:
                
                verification_repo: PostgresBaseRepository[VerificationRequestModel] = uow_postgres.get_repository(VerificationRequestModel)
              
                # Obtener verificaciones pendientes (sin risk_score)
                pending_verifications = await verification_repo.find_all(filter={"status_id": "e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f"})
                for verification in pending_verifications:
                    try:
                        # Evaluar riesgo
                        assessment = await self.assess_risk(verification)
                        
                        # Actualizar en PostgreSQL
                        update_data = {
                            "risk_score": assessment.score,
                            "risk_level_id": self._map_risk_level_to_id(assessment.risk_level),
                            "updated_at": datetime.now()
                        }
                        
                        await verification_repo.update(
                            id= verification.id,
                            data=update_data
                        )
                        
                        async with self._uow_mongo as uow_mongo:
                            try:
                                mongo_repo: MongoBaseRepository[VerificationLogModel] = uow_mongo.get_repository(VerificationLogModel)

                                # Registrar en MongoDB
                                log_entry = VerificationLogModel(
                                    request_id=str(verification.id),
                                    score=assessment.score,
                                    risk_level=assessment.risk_level,
                                    rules_triggered=assessment.rules_triggered,
                                    rules_detail=assessment.rules_detail,
                                    processed_at=datetime.now(),
                                    processing_time_ms=assessment.processing_time_ms
                                )
                                
                                await mongo_repo.insert(log_entry)
                            except Exception as e:
                                raise e
                        
                        stats["processed"] += 1
                        stats["updated"] += 1
                        
                    except Exception as e:
                        print(f"Error procesando verificación {verification.id}: {str(e)}")
                        stats["errors"] += 1
                
                # Confirmar transacción
                await uow_postgres.commit()
                
            except Exception as e:
                await uow_postgres.rollback()
                raise e
            
        return stats

    # HELPERS
    
    def _map_risk_level_to_id(self, risk_level: RiskLevel) -> str:
        """
        Mapea el nivel de riesgo a su UUID correspondiente.
        Estos UUIDs deben coincidir con los de tu tabla risk_level_catalog
        """
        risk_level_mapping = {
            RiskLevel.LOW: "11111111-1111-1111-1111-111111111111",    
            RiskLevel.MEDIUM: "22222222-2222-2222-2222-222222222222",  
            RiskLevel.HIGH: "33333333-3333-3333-3333-333333333333"  
        }
        return risk_level_mapping.get(risk_level, "44444444-4444-4444-4444-444444444444")  # Default
    
    def _check_email_domain(self, data, config: RuleConfig) -> RuleResult:
        """Verifica si el dominio del email está en lista de riesgo"""
        email = getattr(data, 'email', '')
        domain = email.split('@')[-1].lower() if '@' in email else ''
        
        is_risky = domain in config.risky_domains
        
        return RuleResult(
            rule_type=RuleType.EMAIL_DOMAIN_RISK,
            triggered=is_risky,
            score_penalty=30 if is_risky else 0,
            details={
                "email": email,
                "domain": domain,
                "is_risky": is_risky
            }
        )

    def _check_country_restricted(self, data, config: RuleConfig) -> RuleResult:
        """Verifica si el país está en lista restringida"""
        country_id = str(getattr(data, 'country_id', ''))
        
        is_restricted = country_id in config.restricted_countries
        
        return RuleResult(
            rule_type=RuleType.COUNTRY_RESTRICTED,
            triggered=is_restricted,
            score_penalty=40 if is_restricted else 0,
            details={
                "country_id": country_id,
                "is_restricted": is_restricted
            }
        )

    def _check_document_length(self, data, config: RuleConfig) -> RuleResult:
        """Verifica si el número de documento cumple con longitud mínima"""
        document_number = getattr(data, 'document_number', '')
        clean_document = ''.join(filter(str.isalnum, document_number))
        
        is_invalid = len(clean_document) < config.min_document_length
        
        return RuleResult(
            rule_type=RuleType.DOCUMENT_LENGTH_INVALID,
            triggered=is_invalid,
            score_penalty=25 if is_invalid else 0,
            details={
                "document_number": document_number,
                "clean_length": len(clean_document),
                "min_required": config.min_document_length,
                "is_valid": not is_invalid
            }
        )

    def _determine_risk_level(self, score: int) -> RiskLevel:
        """Determina el nivel de riesgo basado en el score"""
        if score >= 70:
            return RiskLevel.LOW
        elif score >= 40:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.HIGH
