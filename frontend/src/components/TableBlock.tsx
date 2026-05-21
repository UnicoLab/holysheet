import React, { useMemo, useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TablePagination from '@mui/material/TablePagination';
import TableSortLabel from '@mui/material/TableSortLabel';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import SearchIcon from '@mui/icons-material/Search';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockSpec } from '../types';

interface TableBlockProps {
  block: BlockSpec;
  index: number;
}

type Order = 'asc' | 'desc';

export const TableBlock: React.FC<TableBlockProps> = ({ block }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const { title, data, columns: propColumns, searchable = true, paginated = true } = block.props;

  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [orderBy, setOrderBy] = useState<string>('');
  const [order, setOrder] = useState<Order>('asc');

  const columns: string[] = useMemo(() => {
    if (propColumns && propColumns.length > 0) return propColumns;
    if (data && data.length > 0) return Object.keys(data[0]);
    return [];
  }, [propColumns, data]);

  const filteredData = useMemo(() => {
    if (!data) return [];
    if (!searchTerm) return data;
    const lower = searchTerm.toLowerCase();
    return data.filter((row: Record<string, any>) =>
      columns.some(col => String(row[col] ?? '').toLowerCase().includes(lower))
    );
  }, [data, searchTerm, columns]);

  const sortedData = useMemo(() => {
    if (!orderBy) return filteredData;
    return [...filteredData].sort((a: Record<string, any>, b: Record<string, any>) => {
      const av = a[orderBy];
      const bv = b[orderBy];
      if (av == null && bv == null) return 0;
      if (av == null) return 1;
      if (bv == null) return -1;
      const cmp = typeof av === 'number' && typeof bv === 'number'
        ? av - bv
        : String(av).localeCompare(String(bv));
      return order === 'asc' ? cmp : -cmp;
    });
  }, [filteredData, orderBy, order]);

  const displayData = paginated
    ? sortedData.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
    : sortedData;

  const handleSort = (col: string) => {
    const isAsc = orderBy === col && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(col);
  };

  const formatHeader = (key: string): string => {
    return key
      .replace(/_/g, ' ')
      .replace(/\b\w/g, c => c.toUpperCase());
  };

  const formatValue = (val: any): string => {
    if (val == null) return '—';
    if (typeof val === 'number') {
      return val.toLocaleString(undefined, { maximumFractionDigits: 2 });
    }
    if (typeof val === 'boolean') return val ? 'Yes' : 'No';
    return String(val);
  };

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2, flexWrap: 'wrap', gap: 2 }}>
          {title && (
            <Typography variant="h6" sx={{ fontWeight: 600, fontSize: '1rem' }}>
              {title}
            </Typography>
          )}
          {searchable && (
            <TextField
              size="small"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => { setSearchTerm(e.target.value); setPage(0); }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon sx={{ fontSize: 18, opacity: 0.5 }} />
                  </InputAdornment>
                ),
              }}
              sx={{
                minWidth: 200,
                '& .MuiOutlinedInput-root': {
                  borderRadius: 3,
                  fontSize: 13,
                },
              }}
            />
          )}
        </Box>

        {(!data || data.length === 0) ? (
          <Box sx={{ py: 6, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">No data available</Typography>
          </Box>
        ) : (
          <>
            <TableContainer sx={{ maxHeight: 500 }}>
              <Table stickyHeader size="small">
                <TableHead>
                  <TableRow>
                    {columns.map((col) => (
                      <TableCell
                        key={col}
                        sx={{
                          fontWeight: 700,
                          fontSize: 12,
                          textTransform: 'uppercase',
                          letterSpacing: '0.05em',
                          backgroundColor: isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.02)',
                          borderBottom: `2px solid ${isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`,
                          whiteSpace: 'nowrap',
                        }}
                      >
                        <TableSortLabel
                          active={orderBy === col}
                          direction={orderBy === col ? order : 'asc'}
                          onClick={() => handleSort(col)}
                        >
                          {formatHeader(col)}
                        </TableSortLabel>
                      </TableCell>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {displayData.map((row: Record<string, any>, idx: number) => (
                    <TableRow
                      key={idx}
                      hover
                      sx={{
                        '&:nth-of-type(even)': {
                          backgroundColor: isDark ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.015)',
                        },
                        '&:last-child td': { borderBottom: 0 },
                      }}
                    >
                      {columns.map((col) => (
                        <TableCell key={col} sx={{ fontSize: 13, py: 1.5 }}>
                          {formatValue(row[col])}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            {paginated && (
              <TablePagination
                component="div"
                count={sortedData.length}
                page={page}
                onPageChange={(_, newPage) => setPage(newPage)}
                rowsPerPage={rowsPerPage}
                onRowsPerPageChange={(e) => { setRowsPerPage(parseInt(e.target.value, 10)); setPage(0); }}
                rowsPerPageOptions={[5, 10, 25, 50]}
                sx={{ borderTop: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)'}` }}
              />
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
};
