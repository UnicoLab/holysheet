import React, { createContext, useContext } from 'react';
import type { ReportFeatures, ThemeName } from './types';

// ─── Features Context ─────────────────────────────────────────────────────────

interface FeaturesContextValue {
  features: ReportFeatures;
  currentTheme: ThemeName;
  toggleTheme: () => void;
}

const FeaturesContext = createContext<FeaturesContextValue>({
  features: {},
  currentTheme: 'dark',
  toggleTheme: () => {},
});

export const FeaturesProvider = FeaturesContext.Provider;

export function useFeatures(): FeaturesContextValue {
  return useContext(FeaturesContext);
}
