export function formatDate(dateStr: string) {
  const d = new Date(dateStr);
  return d.toLocaleDateString("es-MX"); 
}