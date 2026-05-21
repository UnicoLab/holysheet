import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';
import { useTheme, alpha } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Google Sheet Block ───────────────────────────────────────────────────────

const GOOGLE_GREEN = '#34a853';

export const GoogleSheetBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const { title, data = [], source } = block.props;

  const columns = data.length > 0 ? Object.keys(data[0]) : [];
  const hasError = data.length === 1 && 'error' in data[0];

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${alpha(GOOGLE_GREEN, isDark ? 0.2 : 0.15)}`,
        background: isDark
          ? alpha(GOOGLE_GREEN, 0.04)
          : alpha(GOOGLE_GREEN, 0.02),
        backdropFilter: 'blur(12px)',
        height: '100%',
        position: 'relative',
        overflow: 'hidden',
        transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: isDark
            ? `0 8px 32px ${alpha(GOOGLE_GREEN, 0.15)}`
            : `0 8px 32px ${alpha(GOOGLE_GREEN, 0.1)}`,
          borderColor: alpha(GOOGLE_GREEN, 0.3),
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          <CloudDownloadIcon sx={{ color: GOOGLE_GREEN, fontSize: 20 }} />
          <Typography
            variant="h6"
            sx={{
              fontWeight: 700,
              fontSize: '1rem',
              flex: 1,
              color: 'text.primary',
            }}
          >
            {title}
          </Typography>
          {source && (
            <Chip
              label="Google Sheets"
              size="small"
              sx={{
                backgroundColor: alpha(GOOGLE_GREEN, 0.12),
                color: GOOGLE_GREEN,
                fontWeight: 600,
                fontSize: '0.7rem',
                height: 24,
              }}
            />
          )}
        </Box>

        {hasError ? (
          <Typography
            color="error"
            sx={{ fontStyle: 'italic', fontSize: '0.9rem' }}
          >
            {data[0].error}
          </Typography>
        ) : (
          <TableContainer sx={{ maxHeight: 400 }}>
            <Table size="small" stickyHeader>
              <TableHead>
                <TableRow>
                  {columns.map((col) => (
                    <TableCell
                      key={col}
                      sx={{
                        fontWeight: 700,
                        fontSize: '0.8rem',
                        textTransform: 'uppercase',
                        letterSpacing: '0.03em',
                        backgroundColor: isDark
                          ? alpha(GOOGLE_GREEN, 0.08)
                          : alpha(GOOGLE_GREEN, 0.06),
                        borderBottom: `2px solid ${alpha(GOOGLE_GREEN, 0.2)}`,
                      }}
                    >
                      {col}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {data.slice(0, 100).map((row: Record<string, any>, i: number) => (
                  <TableRow
                    key={i}
                    sx={{
                      '&:nth-of-type(odd)': {
                        backgroundColor: isDark
                          ? alpha(GOOGLE_GREEN, 0.02)
                          : alpha(GOOGLE_GREEN, 0.01),
                      },
                      '&:hover': {
                        backgroundColor: isDark
                          ? alpha(GOOGLE_GREEN, 0.06)
                          : alpha(GOOGLE_GREEN, 0.04),
                      },
                    }}
                  >
                    {columns.map((col) => (
                      <TableCell
                        key={col}
                        sx={{ fontSize: '0.85rem', lineHeight: 1.5 }}
                      >
                        {String(row[col] ?? '')}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </CardContent>
    </Card>
  );
};
