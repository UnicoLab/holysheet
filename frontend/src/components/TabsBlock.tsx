import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import { useTheme, alpha } from '@mui/material/styles';
import { BlockRenderer } from '../registry';
import type { BlockComponentProps } from '../types';

// ─── Tab Panel ────────────────────────────────────────────────────────────────

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index }) => (
  <Box
    role="tabpanel"
    hidden={value !== index}
    sx={{ pt: 2.5 }}
  >
    {value === index && children}
  </Box>
);

// ─── Tabs Block ───────────────────────────────────────────────────────────────

export const TabsBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { tabs } = block.props;
  const isDark = theme.palette.mode === 'dark';
  const accentColor = theme.palette.primary.main;
  const [activeTab, setActiveTab] = useState(0);

  if (!tabs || tabs.length === 0) return null;

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          borderColor: isDark ? 'rgba(99,102,241,0.15)' : 'rgba(99,102,241,0.1)',
        },
      }}
    >
      <CardContent sx={{ p: 3, flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Tabs
          value={activeTab}
          onChange={(_e, v) => setActiveTab(v)}
          variant="scrollable"
          scrollButtons="auto"
          sx={{
            minHeight: 38,
            flexShrink: 0,
            borderBottom: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)'}`,
            '& .MuiTabs-indicator': {
              height: 3,
              borderRadius: '3px 3px 0 0',
              background: `linear-gradient(90deg, ${accentColor}, ${alpha(accentColor, 0.6)})`,
            },
            '& .MuiTab-root': {
              textTransform: 'none',
              fontWeight: 600,
              fontSize: '0.85rem',
              minHeight: 38,
              px: 2,
              color: 'text.secondary',
              '&.Mui-selected': {
                color: accentColor,
              },
            },
          }}
        >
          {tabs.map((tab: any, i: number) => (
            <Tab key={i} label={tab.label} />
          ))}
        </Tabs>
        <Box sx={{ flex: 1, minHeight: 0 }}>
          {tabs.map((tab: any, i: number) => (
            <TabPanel key={i} value={activeTab} index={i}>
              {tab.children && tab.children.length > 0 && (
                <BlockRenderer blocks={tab.children} />
              )}
            </TabPanel>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
};
