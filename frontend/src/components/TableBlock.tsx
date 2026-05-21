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
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import SearchIcon from '@mui/icons-material/Search';
import FileDownloadOutlinedIcon from '@mui/icons-material/FileDownloadOutlined';
import Box from '@mui/material/Box';
import { alpha, useTheme } from '@mui/material/styles';
import { useFeatures } from '../FeaturesContext';
import { downloadCSV } from '../utils/downloadCSV';
import type { BlockSpec, TableColumnFormatting } from '../types';

interface TableBlockProps {
  block: BlockSpec;
  index: number;
}

type Order = 'asc' | 'desc';

export const TableBlock: React.FC<TableBlockProps> = ({ block }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const { features } = useFeatures();
  const {
    title,
    data,
    columns: propColumns,
    searchable = true,
    paginated = true,
    downloadable,
    formatting,
  } = block.props;

  const showDownload = downloadable === true || features.download_buttons === true;
  const columnFormatting: Record<string, TableColumnFormatting> | undefined = formatting;

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

  // Compute per-column max values for data_bar
  const columnMaxValues = useMemo(() => {
    if (!columnFormatting || !data) return {};
    const maxes: Record<string, number> = {};
    for (const col of columns) {
      const fmt = columnFormatting[col];
      if (fmt?.data_bar) {
        let max = 0;
        data.forEach((row: Record<string, any>) => {
          const v = Number(row[col]);
          if (!isNaN(v) && v > max) max = v;
        });
        maxes[col] = max || 1;
      }
    }
    return maxes;
  }, [columnFormatting, data, columns]);

  /**
   * Render a cell with conditional formatting applied.
   */
  const renderFormattedCell = (col: string, val: any) => {
    const fmt = columnFormatting?.[col];
    const displayVal = formatValue(val);

    if (!fmt) {
      return displayVal;
    }

    const strVal = String(val ?? '');
    let bgColor: string | undefined;
    let icon: string | undefined;
    let barWidth = 0;

    // color_map: match value to background color
    if (fmt.color_map) {
      bgColor = fmt.color_map[strVal];
    }

    // icon_map: prepend icon/emoji based on value
    if (fmt.icon_map) {
      icon = fmt.icon_map[strVal];
    }

    // data_bar: proportional background bar
    if (fmt.data_bar && columnMaxValues[col]) {
      const numVal = Number(val);
      if (!isNaN(numVal)) {
        barWidth = (numVal / columnMaxValues[col]) * 100;
      }
    }

    return (
      <Box
        sx={{
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          gap: 0.5,
          px: bgColor ? 0.75 : 0,
          py: bgColor ? 0.25 : 0,
          borderRadius: bgColor ? 1 : 0,
          backgroundColor: bgColor ? alpha(bgColor, isDark ? 0.25 : 0.18) : undefined,
          overflow: 'hidden',
        }}
      >
        {/* Data bar behind text */}
        {fmt.data_bar && barWidth > 0 && (
          <Box
            sx={{
              position: 'absolute',
              left: 0,
              top: 0,
              bottom: 0,
              width: `${barWidth}%`,
              backgroundColor: alpha(theme.palette.primary.main, isDark ? 0.12 : 0.1),
              borderRadius: 1,
              transition: 'width 0.3s ease',
            }}
          />
        )}
        {/* Icon */}
        {icon && (
          <Box component="span" sx={{ position: 'relative', zIndex: 1, fontSize: '0.85rem' }}>
            {icon}
          </Box>
        )}
        {/* Text value */}
        <Box component="span" sx={{ position: 'relative', zIndex: 1 }}>
          {displayVal}
        </Box>
      </Box>
    );
  };

  const handleDownload = () => {
    if (!data || data.length === 0) return;
    const filename = (title || 'table_data').replace(/\s+/g, '_').toLowerCase();
    downloadCSV(data, filename);
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
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {title && (
              <Typography variant="h6" sx={{ fontWeight: 600, fontSize: '1rem' }}>
                {title}
              </Typography>
            )}
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
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
            {showDownload && data && data.length > 0 && (
              <Tooltip title="Download as CSV" arrow>
                <IconButton
                  onClick={handleDownload}
                  size="small"
                  sx={{
                    color: 'text.secondary',
                    border: `1px solid ${isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`,
                    borderRadius: 2,
                    '&:hover': {
                      color: theme.palette.primary.main,
                      borderColor: alpha(theme.palette.primary.main, 0.3),
                      backgroundColor: alpha(theme.palette.primary.main, 0.05),
                    },
                  }}
                >
                  <FileDownloadOutlinedIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            )}
          </Box>
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
                          {columnFormatting?.[col]
                            ? renderFormattedCell(col, row[col])
                            : formatValue(row[col])}
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
