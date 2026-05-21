import React, { useState, useEffect, useCallback, useMemo } from 'react';
import Fab from '@mui/material/Fab';
import Drawer from '@mui/material/Drawer';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import ListAltOutlinedIcon from '@mui/icons-material/ListAltOutlined';
import CloseIcon from '@mui/icons-material/Close';
import TableChartOutlinedIcon from '@mui/icons-material/TableChartOutlined';
import BarChartOutlinedIcon from '@mui/icons-material/BarChartOutlined';
import DashboardOutlinedIcon from '@mui/icons-material/DashboardOutlined';
import TextFieldsOutlinedIcon from '@mui/icons-material/TextFieldsOutlined';
import ViewColumnOutlinedIcon from '@mui/icons-material/ViewColumnOutlined';
import SpeedOutlinedIcon from '@mui/icons-material/SpeedOutlined';
import TimelineOutlinedIcon from '@mui/icons-material/TimelineOutlined';
import CodeOutlinedIcon from '@mui/icons-material/CodeOutlined';
import ImageOutlinedIcon from '@mui/icons-material/ImageOutlined';
import WidgetsOutlinedIcon from '@mui/icons-material/WidgetsOutlined';
import { alpha, useTheme } from '@mui/material/styles';
import type { BlockSpec } from '../types';

// ─── Icon Mapping ─────────────────────────────────────────────────────────────

function getBlockIcon(type: string): React.ReactNode {
  if (type.includes('chart') || type.includes('heatmap') || type.includes('candlestick') || type.includes('sankey') || type.includes('waterfall') || type.includes('box_plot') || type.includes('treemap') || type.includes('funnel') || type.includes('correlation') || type.includes('dag') || type.includes('gantt') || type.includes('radar')) {
    return <BarChartOutlinedIcon fontSize="small" />;
  }
  switch (type) {
    case 'data_table':
      return <TableChartOutlinedIcon fontSize="small" />;
    case 'kpi':
    case 'metric':
    case 'scorecard':
      return <SpeedOutlinedIcon fontSize="small" />;
    case 'markdown':
    case 'callout':
    case 'alert':
      return <TextFieldsOutlinedIcon fontSize="small" />;
    case 'columns':
    case 'tabs':
      return <ViewColumnOutlinedIcon fontSize="small" />;
    case 'timeline':
    case 'stepper':
      return <TimelineOutlinedIcon fontSize="small" />;
    case 'code_block':
    case 'json_viewer':
      return <CodeOutlinedIcon fontSize="small" />;
    case 'image':
    case 'video':
      return <ImageOutlinedIcon fontSize="small" />;
    case 'section':
      return <DashboardOutlinedIcon fontSize="small" />;
    default:
      return <WidgetsOutlinedIcon fontSize="small" />;
  }
}

function getBlockLabel(type: string): string {
  return type
    .replace(/_/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());
}

function getBlockTitle(block: BlockSpec): string {
  const props = block.props;
  return props.title || props.label || props.content?.slice(0, 40) || getBlockLabel(block.type);
}

// ─── ReportNavigator Component ────────────────────────────────────────────────

interface ReportNavigatorProps {
  blocks: BlockSpec[];
}

export const ReportNavigator: React.FC<ReportNavigatorProps> = ({ blocks }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const [open, setOpen] = useState(false);
  const [activeBlockId, setActiveBlockId] = useState<string | null>(null);

  // Only show for reports with > 5 blocks
  if (blocks.length <= 5) return null;

  // Flatten blocks that have ids for navigation
  const navItems = useMemo(() => {
    return blocks
      .filter(b => b.id)
      .map(b => ({
        id: b.id,
        title: getBlockTitle(b),
        type: b.type,
        icon: getBlockIcon(b.type),
        label: getBlockLabel(b.type),
      }));
  }, [blocks]);

  // Track current section via IntersectionObserver
  // eslint-disable-next-line react-hooks/rules-of-hooks
  useEffect(() => {
    const elements = navItems
      .map(item => document.getElementById(`block-${item.id}`))
      .filter(Boolean) as HTMLElement[];

    if (elements.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        // Find the topmost visible entry
        const visible = entries
          .filter(e => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);

        if (visible.length > 0) {
          const id = visible[0].target.id.replace('block-', '');
          setActiveBlockId(id);
        }
      },
      { rootMargin: '-80px 0px -50% 0px', threshold: 0.1 }
    );

    elements.forEach(el => observer.observe(el));
    return () => observer.disconnect();
  }, [navItems]);

  const handleNavigate = useCallback((blockId: string) => {
    const el = document.getElementById(`block-${blockId}`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // Close drawer on mobile
      if (window.innerWidth < 768) {
        setOpen(false);
      }
    }
  }, []);

  return (
    <>
      {/* Floating Action Button */}
      <Tooltip title="Navigate report" placement="left">
        <Fab
          size="medium"
          onClick={() => setOpen(true)}
          className="no-print"
          sx={{
            position: 'fixed',
            bottom: 24,
            right: 24,
            zIndex: theme.zIndex.speedDial,
            backgroundColor: isDark
              ? alpha(theme.palette.primary.main, 0.15)
              : alpha(theme.palette.primary.main, 0.1),
            color: theme.palette.primary.main,
            border: `1px solid ${alpha(theme.palette.primary.main, 0.3)}`,
            backdropFilter: 'blur(12px)',
            boxShadow: `0 4px 20px ${alpha(theme.palette.primary.main, 0.2)}`,
            '&:hover': {
              backgroundColor: alpha(theme.palette.primary.main, 0.25),
            },
          }}
        >
          <ListAltOutlinedIcon />
        </Fab>
      </Tooltip>

      {/* Navigation Drawer */}
      <Drawer
        anchor="right"
        open={open}
        onClose={() => setOpen(false)}
        className="no-print"
        PaperProps={{
          sx: {
            width: { xs: 280, sm: 320 },
            backgroundColor: isDark
              ? alpha(theme.palette.background.paper, 0.95)
              : alpha(theme.palette.background.paper, 0.98),
            backdropFilter: 'blur(16px)',
          },
        }}
      >
        {/* Drawer Header */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            px: 2.5,
            py: 2,
            borderBottom: `1px solid ${isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)'}`,
          }}
        >
          <Typography variant="subtitle1" sx={{ fontWeight: 700, fontSize: '0.95rem' }}>
            Report Navigator
          </Typography>
          <IconButton size="small" onClick={() => setOpen(false)}>
            <CloseIcon fontSize="small" />
          </IconButton>
        </Box>

        {/* Block count */}
        <Box sx={{ px: 2.5, py: 1 }}>
          <Typography variant="caption" color="text.secondary">
            {navItems.length} blocks
          </Typography>
        </Box>

        {/* Block list */}
        <List dense sx={{ px: 1, flex: 1, overflowY: 'auto' }}>
          {navItems.map((item) => {
            const isActive = activeBlockId === item.id;
            return (
              <ListItemButton
                key={item.id}
                onClick={() => handleNavigate(item.id)}
                selected={isActive}
                sx={{
                  borderRadius: 2,
                  mb: 0.5,
                  pl: 2,
                  transition: 'all 0.2s ease',
                  ...(isActive && {
                    backgroundColor: alpha(theme.palette.primary.main, isDark ? 0.12 : 0.08),
                    borderLeft: `3px solid ${theme.palette.primary.main}`,
                    pl: 1.625,
                  }),
                  '&:hover': {
                    backgroundColor: alpha(theme.palette.primary.main, isDark ? 0.08 : 0.05),
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: 36, color: isActive ? theme.palette.primary.main : 'text.secondary' }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.title}
                  primaryTypographyProps={{
                    fontSize: '0.85rem',
                    fontWeight: isActive ? 600 : 400,
                    noWrap: true,
                    color: isActive ? theme.palette.primary.main : 'text.primary',
                  }}
                />
                <Chip
                  label={item.label}
                  size="small"
                  sx={{
                    ml: 1,
                    fontSize: '0.6rem',
                    height: 20,
                    fontWeight: 500,
                    backgroundColor: alpha(
                      isActive ? theme.palette.primary.main : theme.palette.text.secondary,
                      isDark ? 0.12 : 0.08,
                    ),
                    color: isActive ? theme.palette.primary.main : 'text.secondary',
                  }}
                />
              </ListItemButton>
            );
          })}
        </List>
      </Drawer>
    </>
  );
};
