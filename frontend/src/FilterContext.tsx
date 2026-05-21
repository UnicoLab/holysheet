import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';

// ─── Filter Types ─────────────────────────────────────────────────────────────

export interface FilterSpec {
  key: string;
  type: 'dropdown' | 'text' | 'date_range' | 'checkbox';
  label: string;
  options?: any[];
  default?: any;
}

export type FilterValues = Record<string, any>;

interface FilterContextValue {
  filters: FilterSpec[];
  filterValues: FilterValues;
  setFilterValue: (key: string, value: any) => void;
  resetFilters: () => void;
  applyFilters: (data: Record<string, any>[]) => Record<string, any>[];
}

const FilterContext = createContext<FilterContextValue>({
  filters: [],
  filterValues: {},
  setFilterValue: () => {},
  resetFilters: () => {},
  applyFilters: (data) => data,
});

// ─── Provider ─────────────────────────────────────────────────────────────────

interface FilterProviderProps {
  filters: FilterSpec[];
  children: React.ReactNode;
}

export const FilterProvider: React.FC<FilterProviderProps> = ({ filters, children }) => {
  const defaultValues = useMemo(() => {
    const vals: FilterValues = {};
    for (const f of filters) {
      if (f.default !== undefined) {
        vals[f.key] = f.default;
      }
    }
    return vals;
  }, [filters]);

  const [filterValues, setFilterValues] = useState<FilterValues>(defaultValues);

  const setFilterValue = useCallback((key: string, value: any) => {
    setFilterValues((prev) => ({ ...prev, [key]: value }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilterValues(defaultValues);
  }, [defaultValues]);

  const applyFilters = useCallback(
    (data: Record<string, any>[]): Record<string, any>[] => {
      if (!data || data.length === 0) return data;

      return data.filter((row) => {
        for (const f of filters) {
          const val = filterValues[f.key];
          if (val === undefined || val === null || val === '') continue;

          const cellValue = row[f.key];

          switch (f.type) {
            case 'dropdown': {
              if (String(cellValue) !== String(val)) return false;
              break;
            }
            case 'text': {
              if (!String(cellValue ?? '').toLowerCase().includes(String(val).toLowerCase())) {
                return false;
              }
              break;
            }
            case 'date_range': {
              if (Array.isArray(val) && val.length === 2) {
                const cellDate = String(cellValue ?? '');
                const [from, to] = val;
                if (from && cellDate < from) return false;
                if (to && cellDate > to) return false;
              }
              break;
            }
            case 'checkbox': {
              if (Array.isArray(val) && val.length > 0) {
                if (!val.includes(String(cellValue))) return false;
              }
              break;
            }
          }
        }
        return true;
      });
    },
    [filters, filterValues],
  );

  const value = useMemo(
    () => ({ filters, filterValues, setFilterValue, resetFilters, applyFilters }),
    [filters, filterValues, setFilterValue, resetFilters, applyFilters],
  );

  return <FilterContext.Provider value={value}>{children}</FilterContext.Provider>;
};

// ─── Hook ─────────────────────────────────────────────────────────────────────

export function useFilters(): FilterContextValue {
  return useContext(FilterContext);
}
