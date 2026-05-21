import React, { useState, useEffect, useCallback } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import LinearProgress from '@mui/material/LinearProgress';
import CloseIcon from '@mui/icons-material/Close';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { alpha, useTheme } from '@mui/material/styles';
import { motion, AnimatePresence } from 'framer-motion';
import { BlockRenderer } from '../registry';
import type { BlockSpec } from '../types';

// ─── Presentation Mode ────────────────────────────────────────────────────────

interface PresentationModeProps {
  blocks: BlockSpec[];
  onExit: () => void;
}

/**
 * Extracts "slides" from the block list. Each Section block becomes a slide.
 * Non-section blocks at the top level are grouped into an "Intro" slide.
 */
function extractSlides(blocks: BlockSpec[]): { title: string; blocks: BlockSpec[] }[] {
  const slides: { title: string; blocks: BlockSpec[] }[] = [];
  let introBlocks: BlockSpec[] = [];

  for (const block of blocks) {
    if (block.type === 'section') {
      // Flush intro
      if (introBlocks.length > 0) {
        slides.push({ title: 'Overview', blocks: introBlocks });
        introBlocks = [];
      }
      slides.push({
        title: block.props.title || `Section ${slides.length + 1}`,
        blocks: [block],
      });
    } else {
      introBlocks.push(block);
    }
  }

  if (introBlocks.length > 0) {
    slides.push({ title: 'Overview', blocks: introBlocks });
  }

  // If no sections found, put everything in one slide
  if (slides.length === 0) {
    slides.push({ title: 'All Content', blocks });
  }

  return slides;
}

export const PresentationMode: React.FC<PresentationModeProps> = ({ blocks, onExit }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const accentColor = theme.palette.primary.main;

  const slides = React.useMemo(() => extractSlides(blocks), [blocks]);
  const [currentSlide, setCurrentSlide] = useState(0);
  const totalSlides = slides.length;

  const goNext = useCallback(() => {
    setCurrentSlide((prev) => Math.min(prev + 1, totalSlides - 1));
  }, [totalSlides]);

  const goPrev = useCallback(() => {
    setCurrentSlide((prev) => Math.max(prev - 1, 0));
  }, []);

  // Request fullscreen on mount, exit on unmount
  useEffect(() => {
    const el = document.documentElement;
    try {
      el.requestFullscreen?.();
    } catch {
      // Fullscreen may not be available
    }
    return () => {
      try {
        if (document.fullscreenElement) {
          document.exitFullscreen?.();
        }
      } catch {
        // ignore
      }
    };
  }, []);

  // Listen for fullscreen exit to trigger onExit
  useEffect(() => {
    const handler = () => {
      if (!document.fullscreenElement) {
        onExit();
      }
    };
    document.addEventListener('fullscreenchange', handler);
    return () => document.removeEventListener('fullscreenchange', handler);
  }, [onExit]);

  // Keyboard navigation
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowRight':
        case 'ArrowDown':
        case ' ':
          e.preventDefault();
          goNext();
          break;
        case 'ArrowLeft':
        case 'ArrowUp':
          e.preventDefault();
          goPrev();
          break;
        case 'Escape':
          e.preventDefault();
          onExit();
          break;
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [goNext, goPrev, onExit]);

  const slide = slides[currentSlide];
  const progress = totalSlides > 1 ? ((currentSlide + 1) / totalSlides) * 100 : 100;

  return (
    <Box
      onClick={goNext}
      sx={{
        position: 'fixed',
        inset: 0,
        zIndex: 9999,
        bgcolor: isDark ? '#0a0a0f' : '#F5F7FA',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
      }}
    >
      {/* Top bar */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          px: 3,
          py: 1.5,
          borderBottom: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)'}`,
          flexShrink: 0,
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <Typography variant="caption" sx={{ color: 'text.secondary', fontWeight: 600, letterSpacing: '0.05em' }}>
          {slide.title}
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography variant="caption" sx={{ color: 'text.secondary' }}>
            {currentSlide + 1} / {totalSlides}
          </Typography>
          <IconButton
            onClick={(e) => { e.stopPropagation(); onExit(); }}
            size="small"
            sx={{
              color: 'text.secondary',
              '&:hover': { color: 'error.main' },
            }}
          >
            <CloseIcon fontSize="small" />
          </IconButton>
        </Box>
      </Box>

      {/* Content area */}
      <Box
        sx={{
          flex: 1,
          overflow: 'auto',
          px: { xs: 2, sm: 4, md: 8 },
          py: 4,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}
      >
        <AnimatePresence mode="wait">
          <motion.div
            key={currentSlide}
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -40 }}
            transition={{ duration: 0.3, ease: 'easeInOut' }}
            style={{ maxWidth: 1400, width: '100%', margin: '0 auto' }}
          >
            <BlockRenderer blocks={slide.blocks} />
          </motion.div>
        </AnimatePresence>
      </Box>

      {/* Navigation bar at bottom */}
      <Box
        sx={{ flexShrink: 0 }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Nav buttons */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 2,
            py: 1,
          }}
        >
          <IconButton
            onClick={goPrev}
            disabled={currentSlide === 0}
            sx={{
              color: 'text.secondary',
              border: `1px solid ${isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`,
              borderRadius: 2,
              '&:hover': {
                color: accentColor,
                borderColor: alpha(accentColor, 0.3),
              },
            }}
          >
            <NavigateBeforeIcon />
          </IconButton>
          <IconButton
            onClick={goNext}
            disabled={currentSlide === totalSlides - 1}
            sx={{
              color: 'text.secondary',
              border: `1px solid ${isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`,
              borderRadius: 2,
              '&:hover': {
                color: accentColor,
                borderColor: alpha(accentColor, 0.3),
              },
            }}
          >
            <NavigateNextIcon />
          </IconButton>
        </Box>

        {/* Progress bar */}
        <LinearProgress
          variant="determinate"
          value={progress}
          sx={{
            height: 3,
            backgroundColor: isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)',
            '& .MuiLinearProgress-bar': {
              backgroundColor: accentColor,
              transition: 'transform 0.3s ease',
            },
          }}
        />
      </Box>
    </Box>
  );
};
