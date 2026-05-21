import React, { useState, useCallback } from 'react';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { useTheme } from '@mui/material/styles';
import { Layout } from './components/Layout';
import { BlockRenderer } from './registry';
import { PresentationMode } from './components/PresentationMode';
import { ReportNavigator } from './components/ReportNavigator';
import { PWAInstall } from './components/PWAInstall';
import { FeaturesProvider } from './FeaturesContext';
import { FilterProvider } from './FilterContext';
import { FilterBar } from './components/FilterBar';
import type { ReportSpec, ThemeName, PageSpec, BlockSpec } from './types';

// ─── Multi-page tab panel ─────────────────────────────────────────────────────

interface PageTabPanelProps {
  children: React.ReactNode;
  index: number;
  value: number;
}

const PageTabPanel: React.FC<PageTabPanelProps> = ({ children, value, index }) => (
  <div role="tabpanel" hidden={value !== index} style={{ display: value === index ? 'block' : 'none' }}>
    {value === index && children}
  </div>
);

// ─── App ──────────────────────────────────────────────────────────────────────

interface AppProps {
  spec: ReportSpec;
  currentTheme: ThemeName;
  onToggleTheme: () => void;
}

const App: React.FC<AppProps> = ({ spec, currentTheme, onToggleTheme }) => {
  const features = spec.features ?? {};
  const isMultiPage = features.multi_page === true;
  const [presentationActive, setPresentationActive] = useState(false);
  const [activePage, setActivePage] = useState(0);
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';

  const handleEnterPresentation = useCallback(() => {
    setPresentationActive(true);
  }, []);

  const handleExitPresentation = useCallback(() => {
    setPresentationActive(false);
  }, []);

  // For multi-page, blocks is an array of { label, blocks } objects
  const pages = isMultiPage
    ? (spec.blocks as unknown as PageSpec[])
    : null;

  // Flatten all blocks for presentation mode
  const allBlocks = isMultiPage
    ? (pages || []).flatMap((p) => p.blocks)
    : (spec.blocks as BlockSpec[]);

  // Resolve filters from features.filters or top-level spec.filters
  const filterSpecs = features.filters ?? (spec as any).filters ?? [];

  return (
    <FeaturesProvider value={{ features, currentTheme, toggleTheme: onToggleTheme }}>
      <FilterProvider filters={filterSpecs}>
        {presentationActive && (
          <PresentationMode
            blocks={allBlocks}
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
            <FilterBar />
            {isMultiPage && pages ? (
              <>
                <Box
                  sx={{
                    mb: 3,
                    borderBottom: 1,
                    borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'divider',
                    background: isDark
                      ? 'rgba(255,255,255,0.03)'
                      : 'rgba(0,0,0,0.01)',
                    borderRadius: '12px 12px 0 0',
                  }}
                >
                  <Tabs
                    value={activePage}
                    onChange={(_, v) => setActivePage(v)}
                    variant="scrollable"
                    scrollButtons="auto"
                    sx={{
                      '& .MuiTab-root': {
                        fontWeight: 600,
                        textTransform: 'none',
                        fontSize: '0.95rem',
                        minHeight: 48,
                      },
                    }}
                  >
                    {pages.map((page, i) => (
                      <Tab key={i} label={page.label} />
                    ))}
                  </Tabs>
                </Box>
                {pages.map((page, i) => (
                  <PageTabPanel key={i} value={activePage} index={i}>
                    <BlockRenderer blocks={page.blocks} />
                  </PageTabPanel>
                ))}
              </>
            ) : (
              <BlockRenderer blocks={spec.blocks as BlockSpec[]} />
            )}
          </Container>
        </Layout>

        {/* Report Navigator (mini-map) — self-hides when ≤5 blocks */}
        <ReportNavigator blocks={allBlocks} />

        {/* PWA Install banner — only when pwa_mode feature is enabled */}
        {features.pwa_mode === true && <PWAInstall />}
      </FilterProvider>
    </FeaturesProvider>
  );
};

export default App;
