import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import RefreshIcon from '@mui/icons-material/Refresh';
import FilterListIcon from '@mui/icons-material/FilterList';
import { useTheme } from '@mui/material/styles';
import { useFilters } from '../FilterContext';
import type { FilterSpec } from '../FilterContext';

// ─── Filter Controls ──────────────────────────────────────────────────────────

const DropdownFilter: React.FC<{ spec: FilterSpec }> = ({ spec }) => {
  const { filterValues, setFilterValue } = useFilters();
  const value = filterValues[spec.key] ?? '';

  return (
    <FormControl size="small" sx={{ minWidth: 150 }}>
      <InputLabel>{spec.label}</InputLabel>
      <Select
        value={value}
        label={spec.label}
        onChange={(e) => setFilterValue(spec.key, e.target.value)}
        sx={{ borderRadius: 2, fontSize: 13 }}
      >
        <MenuItem value="">
          <em>All</em>
        </MenuItem>
        {(spec.options ?? []).map((opt: any) => (
          <MenuItem key={String(opt)} value={String(opt)}>
            {String(opt)}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

const TextFilter: React.FC<{ spec: FilterSpec }> = ({ spec }) => {
  const { filterValues, setFilterValue } = useFilters();
  const value = filterValues[spec.key] ?? '';

  return (
    <TextField
      size="small"
      label={spec.label}
      value={value}
      onChange={(e) => setFilterValue(spec.key, e.target.value)}
      sx={{
        minWidth: 150,
        '& .MuiOutlinedInput-root': { borderRadius: 2, fontSize: 13 },
      }}
    />
  );
};

const DateRangeFilter: React.FC<{ spec: FilterSpec }> = ({ spec }) => {
  const { filterValues, setFilterValue } = useFilters();
  const value = filterValues[spec.key] ?? ['', ''];
  const from = Array.isArray(value) ? value[0] ?? '' : '';
  const to = Array.isArray(value) ? value[1] ?? '' : '';

  return (
    <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
      <Typography variant="caption" sx={{ fontWeight: 600, whiteSpace: 'nowrap' }}>
        {spec.label}
      </Typography>
      <TextField
        size="small"
        type="date"
        label="From"
        value={from}
        onChange={(e) => setFilterValue(spec.key, [e.target.value, to])}
        InputLabelProps={{ shrink: true }}
        sx={{
          minWidth: 130,
          '& .MuiOutlinedInput-root': { borderRadius: 2, fontSize: 13 },
        }}
      />
      <TextField
        size="small"
        type="date"
        label="To"
        value={to}
        onChange={(e) => setFilterValue(spec.key, [from, e.target.value])}
        InputLabelProps={{ shrink: true }}
        sx={{
          minWidth: 130,
          '& .MuiOutlinedInput-root': { borderRadius: 2, fontSize: 13 },
        }}
      />
    </Box>
  );
};

const CheckboxFilter: React.FC<{ spec: FilterSpec }> = ({ spec }) => {
  const { filterValues, setFilterValue } = useFilters();
  const selected: string[] = filterValues[spec.key] ?? [];

  const handleToggle = (optVal: string) => {
    const next = selected.includes(optVal)
      ? selected.filter((v) => v !== optVal)
      : [...selected, optVal];
    setFilterValue(spec.key, next);
  };

  return (
    <Box>
      <Typography variant="caption" sx={{ fontWeight: 600, mb: 0.5, display: 'block' }}>
        {spec.label}
      </Typography>
      <FormGroup row>
        {(spec.options ?? []).map((opt: any) => (
          <FormControlLabel
            key={String(opt)}
            control={
              <Checkbox
                size="small"
                checked={selected.includes(String(opt))}
                onChange={() => handleToggle(String(opt))}
              />
            }
            label={String(opt)}
            sx={{ '& .MuiTypography-root': { fontSize: 13 } }}
          />
        ))}
      </FormGroup>
    </Box>
  );
};

// ─── FilterBar ────────────────────────────────────────────────────────────────

export const FilterBar: React.FC = () => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const { filters, resetFilters } = useFilters();

  if (!filters || filters.length === 0) return null;

  return (
    <Box
      sx={{
        position: 'sticky',
        top: 0,
        zIndex: 1100,
        display: 'flex',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: 2,
        px: 3,
        py: 1.5,
        mb: 2,
        borderRadius: 3,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)'}`,
        background: isDark
          ? 'rgba(15, 15, 25, 0.75)'
          : 'rgba(255, 255, 255, 0.65)',
        backdropFilter: 'blur(16px) saturate(180%)',
        WebkitBackdropFilter: 'blur(16px) saturate(180%)',
        boxShadow: isDark
          ? '0 4px 30px rgba(0,0,0,0.3)'
          : '0 4px 30px rgba(0,0,0,0.08)',
      }}
    >
      <FilterListIcon sx={{ color: 'text.secondary', fontSize: 20 }} />
      {filters.map((f) => {
        switch (f.type) {
          case 'dropdown':
            return <DropdownFilter key={f.key} spec={f} />;
          case 'text':
            return <TextFilter key={f.key} spec={f} />;
          case 'date_range':
            return <DateRangeFilter key={f.key} spec={f} />;
          case 'checkbox':
            return <CheckboxFilter key={f.key} spec={f} />;
          default:
            return null;
        }
      })}
      <Tooltip title="Reset all filters" arrow>
        <IconButton onClick={resetFilters} size="small" sx={{ ml: 'auto' }}>
          <RefreshIcon fontSize="small" />
        </IconButton>
      </Tooltip>
    </Box>
  );
};
