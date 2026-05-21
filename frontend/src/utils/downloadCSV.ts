// ─── CSV Download Utility ─────────────────────────────────────────────────────

/**
 * Convert an array of objects to a CSV string and trigger a browser download.
 */
export function downloadCSV(data: Record<string, any>[], filename: string): void {
  if (!data || data.length === 0) return;

  const columns = Object.keys(data[0]);
  const escapeCell = (val: any): string => {
    const str = val == null ? '' : String(val);
    // Escape quotes and wrap in quotes if the cell contains commas, quotes, or newlines
    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
      return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
  };

  const header = columns.map(escapeCell).join(',');
  const rows = data.map((row) =>
    columns.map((col) => escapeCell(row[col])).join(',')
  );

  const csv = [header, ...rows].join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${filename}.csv`;
  link.style.display = 'none';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
