import React, { useState, useCallback } from 'react';
import Container from '@mui/material/Container';
import { Layout } from './components/Layout';
import { BlockRenderer } from './registry';
import { PresentationMode } from './components/PresentationMode';
import { FeaturesProvider } from './FeaturesContext';
import type { ReportSpec, ThemeName } from './types';

// ─── App ──────────────────────────────────────────────────────────────────────

interface AppProps {
  spec: ReportSpec;
  currentTheme: ThemeName;
  onToggleTheme: () => void;
}

const App: React.FC<AppProps> = ({ spec, currentTheme, onToggleTheme }) => {
  const features = spec.features ?? {};
  const [presentationActive, setPresentationActive] = useState(false);

  const handleEnterPresentation = useCallback(() => {
    setPresentationActive(true);
  }, []);

  const handleExitPresentation = useCallback(() => {
    setPresentationActive(false);
  }, []);

  return (
    <FeaturesProvider value={{ features, currentTheme, toggleTheme: onToggleTheme }}>
      {presentationActive && (
        <PresentationMode
          blocks={spec.blocks}
          onExit={handleExitPresentation}
        />
      )}
      <Layout
        spec={spec}
        showThemeToggle={features.theme_switch === true}
        showPresentationButton={features.presentation_mode === true}
        currentTheme={currentTheme}
        onToggleTheme={onToggleTheme}
        onEnterPresentation={handleEnterPresentation}
      >
        <Container maxWidth="xl" sx={{ py: 4 }}>
          <BlockRenderer blocks={spec.blocks} />
        </Container>
      </Layout>
    </FeaturesProvider>
  );
};

export default App;
