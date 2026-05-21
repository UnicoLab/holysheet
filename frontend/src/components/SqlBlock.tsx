import React, { useState, useMemo, useCallback } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import { useTheme } from '@mui/material/styles';
import type { BlockSpec } from '../types';

interface SqlBlockProps {
  block: BlockSpec;
  index: number;
}

// ─── Lightweight SQL Engine ───────────────────────────────────────────────────

interface ParsedQuery {
  columns: string[] | '*';
  aggregates: { alias: string; fn: string; col: string }[];
  where: { col: string; op: string; val: string }[];
  orderBy: { col: string; dir: 'asc' | 'desc' }[];
  groupBy: string[];
  limit: number | null;
}

function parseSQL(sql: string): ParsedQuery {
  const q = sql.trim().replace(/;$/, '');
  const tokens = q.replace(/\s+/g, ' ');

  const result: ParsedQuery = {
    columns: '*',
    aggregates: [],
    where: [],
    orderBy: [],
    groupBy: [],
    limit: null,
  };

  // Extract LIMIT
  const limitMatch = tokens.match(/\bLIMIT\s+(\d+)/i);
  if (limitMatch) result.limit = parseInt(limitMatch[1], 10);

  // Extract ORDER BY
  const orderMatch = tokens.match(/\bORDER\s+BY\s+(.+?)(?:\s+LIMIT\b|$)/i);
  if (orderMatch) {
    orderMatch[1].split(',').forEach((part) => {
      const parts = part.trim().split(/\s+/);
      result.orderBy.push({
        col: parts[0],
        dir: (parts[1]?.toLowerCase() === 'desc' ? 'desc' : 'asc'),
      });
    });
  }

  // Extract GROUP BY
  const groupMatch = tokens.match(/\bGROUP\s+BY\s+(.+?)(?:\s+ORDER\b|\s+LIMIT\b|$)/i);
  if (groupMatch) {
    result.groupBy = groupMatch[1].split(',').map((c) => c.trim());
  }

  // Extract WHERE
  const whereMatch = tokens.match(/\bWHERE\s+(.+?)(?:\s+GROUP\b|\s+ORDER\b|\s+LIMIT\b|$)/i);
  if (whereMatch) {
    const clauses = whereMatch[1].split(/\s+AND\s+/i);
    clauses.forEach((clause) => {
      const m = clause.trim().match(/^(\w+)\s*(>=|<=|!=|<>|=|>|<|LIKE)\s*'?([^']*)'?$/i);
      if (m) {
        result.where.push({ col: m[1], op: m[2].toUpperCase(), val: m[3] });
      }
    });
  }

  // Extract SELECT columns
  const selectMatch = tokens.match(/^SELECT\s+(.+?)\s+FROM\b/i);
  if (selectMatch) {
    const colStr = selectMatch[1].trim();
    if (colStr === '*') {
      result.columns = '*';
    } else {
      const cols: string[] = [];
      colStr.split(',').forEach((part) => {
        const p = part.trim();
        const aggMatch = p.match(/^(COUNT|SUM|AVG|MIN|MAX)\((\w+|\*)\)(?:\s+AS\s+(\w+))?$/i);
        if (aggMatch) {
          result.aggregates.push({
            fn: aggMatch[1].toUpperCase(),
            col: aggMatch[2],
            alias: aggMatch[3] ?? `${aggMatch[1].toLowerCase()}_${aggMatch[2]}`,
          });
        } else {
          const aliasMatch = p.match(/^(\w+)(?:\s+AS\s+(\w+))?$/i);
          if (aliasMatch) cols.push(aliasMatch[1]);
        }
      });
      if (cols.length > 0 || result.aggregates.length > 0) {
        result.columns = cols.length > 0 ? cols : '*';
      }
    }
  }

  return result;
}

function evaluateWhere(row: Record<string, any>, conditions: ParsedQuery['where']): boolean {
  return conditions.every(({ col, op, val }) => {
    const cell = row[col];
    const numCell = Number(cell);
    const numVal = Number(val);
    const isNum = !isNaN(numCell) && !isNaN(numVal);

    switch (op) {
      case '=': return String(cell) === val;
      case '!=':
      case '<>': return String(cell) !== val;
      case '>': return isNum && numCell > numVal;
      case '<': return isNum && numCell < numVal;
      case '>=': return isNum && numCell >= numVal;
      case '<=': return isNum && numCell <= numVal;
      case 'LIKE': {
        const pattern = val.replace(/%/g, '.*').replace(/_/g, '.');
        return new RegExp(`^${pattern}$`, 'i').test(String(cell ?? ''));
      }
      default: return true;
    }
  });
}

function executeQuery(data: Record<string, any>[], parsed: ParsedQuery): Record<string, any>[] {
  if (!data || data.length === 0) return [];

  // 1. WHERE
  let rows = parsed.where.length > 0
    ? data.filter((r) => evaluateWhere(r, parsed.where))
    : [...data];

  // 2. GROUP BY + aggregates
  if (parsed.groupBy.length > 0 && parsed.aggregates.length > 0) {
    const groups = new Map<string, Record<string, any>[]>();
    rows.forEach((row) => {
      const key = parsed.groupBy.map((c) => String(row[c] ?? '')).join('||');
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key)!.push(row);
    });

    rows = Array.from(groups.entries()).map(([, groupRows]) => {
      const result: Record<string, any> = {};
      parsed.groupBy.forEach((c) => { result[c] = groupRows[0][c]; });
      parsed.aggregates.forEach(({ fn, col, alias }) => {
        switch (fn) {
          case 'COUNT': result[alias] = groupRows.length; break;
          case 'SUM': result[alias] = groupRows.reduce((s, r) => s + Number(r[col] ?? 0), 0); break;
          case 'AVG': result[alias] = groupRows.reduce((s, r) => s + Number(r[col] ?? 0), 0) / groupRows.length; break;
          case 'MIN': result[alias] = Math.min(...groupRows.map((r) => Number(r[col] ?? Infinity))); break;
          case 'MAX': result[alias] = Math.max(...groupRows.map((r) => Number(r[col] ?? -Infinity))); break;
        }
      });
      return result;
    });
  } else if (parsed.aggregates.length > 0) {
    // Aggregates without GROUP BY → single result row
    const result: Record<string, any> = {};
    parsed.aggregates.forEach(({ fn, col, alias }) => {
      switch (fn) {
        case 'COUNT': result[alias] = rows.length; break;
        case 'SUM': result[alias] = rows.reduce((s, r) => s + Number(r[col] ?? 0), 0); break;
        case 'AVG': result[alias] = rows.reduce((s, r) => s + Number(r[col] ?? 0), 0) / (rows.length || 1); break;
        case 'MIN': result[alias] = Math.min(...rows.map((r) => Number(r[col] ?? Infinity))); break;
        case 'MAX': result[alias] = Math.max(...rows.map((r) => Number(r[col] ?? -Infinity))); break;
      }
    });
    rows = [result];
  }

  // 3. SELECT projection
  if (parsed.columns !== '*' && parsed.columns.length > 0 && parsed.aggregates.length === 0) {
    rows = rows.map((row) => {
      const result: Record<string, any> = {};
      (parsed.columns as string[]).forEach((c) => { result[c] = row[c]; });
      return result;
    });
  }

  // 4. ORDER BY
  if (parsed.orderBy.length > 0) {
    rows.sort((a, b) => {
      for (const { col, dir } of parsed.orderBy) {
        const av = a[col], bv = b[col];
        const cmp = typeof av === 'number' && typeof bv === 'number'
          ? av - bv
          : String(av ?? '').localeCompare(String(bv ?? ''));
        if (cmp !== 0) return dir === 'asc' ? cmp : -cmp;
      }
      return 0;
    });
  }

  // 5. LIMIT
  if (parsed.limit !== null) {
    rows = rows.slice(0, parsed.limit);
  }

  return rows;
}

// ─── SQL Syntax Highlight ─────────────────────────────────────────────────────

function highlightSQL(sql: string, isDark: boolean): React.ReactNode {
  const keywords = /\b(SELECT|FROM|WHERE|AND|OR|ORDER\s+BY|GROUP\s+BY|LIMIT|AS|COUNT|SUM|AVG|MIN|MAX|LIKE|IN|NOT|NULL|IS|ASC|DESC|HAVING|JOIN|ON|LEFT|RIGHT|INNER|OUTER|DISTINCT)\b/gi;
  const parts = sql.split(keywords);
  return parts.map((part, i) => {
    if (keywords.test(part)) {
      return (
        <span key={i} style={{ color: isDark ? '#818cf8' : '#4f46e5', fontWeight: 700 }}>
          {part.toUpperCase()}
        </span>
      );
    }
    // Reset regex lastIndex after test
    keywords.lastIndex = 0;
    if (/\b(SELECT|FROM|WHERE|AND|OR|ORDER\s+BY|GROUP\s+BY|LIMIT|AS|COUNT|SUM|AVG|MIN|MAX|LIKE|IN|NOT|NULL|IS|ASC|DESC|HAVING|JOIN|ON|LEFT|RIGHT|INNER|OUTER|DISTINCT)\b/i.test(part)) {
      return (
        <span key={i} style={{ color: isDark ? '#818cf8' : '#4f46e5', fontWeight: 700 }}>
          {part.toUpperCase()}
        </span>
      );
    }
    return <span key={i}>{part}</span>;
  });
}

// ─── Component ────────────────────────────────────────────────────────────────

export const SqlBlock: React.FC<SqlBlockProps> = ({ block }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const { title, query, data } = block.props;

  const [results, setResults] = useState<Record<string, any>[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRun = useCallback(() => {
    try {
      const parsed = parseSQL(query);
      const result = executeQuery(data ?? [], parsed);
      setResults(result);
      setError(null);
    } catch (e: any) {
      setError(e.message || 'Query execution failed');
      setResults(null);
    }
  }, [query, data]);

  const resultColumns = useMemo(() => {
    if (!results || results.length === 0) return [];
    return Object.keys(results[0]);
  }, [results]);

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
        height: '100%',
        transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: isDark
            ? '0 8px 32px rgba(99,102,241,0.12)'
            : '0 8px 32px rgba(0,0,0,0.06)',
          borderColor: isDark ? 'rgba(99,102,241,0.2)' : 'rgba(99,102,241,0.15)',
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        {title && (
          <Typography variant="h6" sx={{ fontWeight: 600, fontSize: '1rem', mb: 2 }}>
            {title}
          </Typography>
        )}

        {/* SQL Query Display */}
        <Box
          sx={{
            p: 2,
            mb: 2,
            borderRadius: 2,
            backgroundColor: isDark ? 'rgba(0,0,0,0.4)' : 'rgba(0,0,0,0.04)',
            border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)'}`,
            fontFamily: '"Fira Code", "Cascadia Code", "Consolas", monospace',
            fontSize: 13,
            lineHeight: 1.7,
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
            overflowX: 'auto',
          }}
        >
          {highlightSQL(query ?? '', isDark)}
        </Box>

        {/* Run Button */}
        <Button
          variant="contained"
          size="small"
          startIcon={<PlayArrowIcon />}
          onClick={handleRun}
          sx={{
            mb: 2,
            borderRadius: 2,
            textTransform: 'none',
            fontWeight: 600,
            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
            '&:hover': {
              background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
            },
          }}
        >
          Run Query
        </Button>

        {/* Error */}
        {error && (
          <Typography variant="body2" color="error" sx={{ mb: 2 }}>
            ⚠ {error}
          </Typography>
        )}

        {/* Results Table */}
        {results && results.length > 0 && (
          <TableContainer sx={{ maxHeight: 400 }}>
            <Table stickyHeader size="small">
              <TableHead>
                <TableRow>
                  {resultColumns.map((col) => (
                    <TableCell
                      key={col}
                      sx={{
                        fontWeight: 700,
                        fontSize: 12,
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em',
                        backgroundColor: isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.02)',
                        borderBottom: `2px solid ${isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`,
                      }}
                    >
                      {col.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {results.map((row, idx) => (
                  <TableRow
                    key={idx}
                    hover
                    sx={{
                      '&:nth-of-type(even)': {
                        backgroundColor: isDark ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.015)',
                      },
                    }}
                  >
                    {resultColumns.map((col) => (
                      <TableCell key={col} sx={{ fontSize: 13, py: 1.5 }}>
                        {row[col] == null
                          ? '—'
                          : typeof row[col] === 'number'
                            ? row[col].toLocaleString(undefined, { maximumFractionDigits: 2 })
                            : String(row[col])}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}

        {results && results.length === 0 && (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 3 }}>
            No results returned
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};
