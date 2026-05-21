import React, { useState, useEffect, useRef, useCallback } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import PauseIcon from '@mui/icons-material/Pause';
import StopIcon from '@mui/icons-material/Stop';
import { useTheme, keyframes } from '@mui/material/styles';
import type { BlockSpec } from '../types';

interface NarrationBlockProps {
  block: BlockSpec;
  index: number;
}

// ─── Audio wave animation ─────────────────────────────────────────────────────

const wave = keyframes`
  0%, 100% { transform: scaleY(0.3); }
  50% { transform: scaleY(1); }
`;

const WaveBars: React.FC<{ active: boolean; isDark: boolean }> = ({ active, isDark }) => (
  <Box
    sx={{
      display: 'flex',
      alignItems: 'center',
      gap: '3px',
      height: 24,
      mx: 1,
    }}
  >
    {[0, 1, 2, 3, 4].map((i) => (
      <Box
        key={i}
        sx={{
          width: 3,
          height: '100%',
          borderRadius: 2,
          backgroundColor: isDark ? 'rgba(139,92,246,0.7)' : 'rgba(99,102,241,0.7)',
          transformOrigin: 'bottom',
          animation: active ? `${wave} 0.8s ease-in-out ${i * 0.1}s infinite` : 'none',
          transform: active ? undefined : 'scaleY(0.3)',
          transition: 'transform 0.3s ease',
        }}
      />
    ))}
  </Box>
);

// ─── Component ────────────────────────────────────────────────────────────────

export const NarrationBlock: React.FC<NarrationBlockProps> = ({ block }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const { text, autoplay } = block.props;

  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);
  const mountedRef = useRef(true);

  useEffect(() => {
    return () => {
      mountedRef.current = false;
      window.speechSynthesis.cancel();
    };
  }, []);

  const handlePlay = useCallback(() => {
    if (!text || !window.speechSynthesis) return;

    if (isPaused) {
      window.speechSynthesis.resume();
      setIsPaused(false);
      setIsPlaying(true);
      return;
    }

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    utterance.pitch = 1;
    utterance.onend = () => {
      if (mountedRef.current) {
        setIsPlaying(false);
        setIsPaused(false);
      }
    };
    utterance.onerror = () => {
      if (mountedRef.current) {
        setIsPlaying(false);
        setIsPaused(false);
      }
    };

    utteranceRef.current = utterance;
    window.speechSynthesis.speak(utterance);
    setIsPlaying(true);
    setIsPaused(false);
  }, [text, isPaused]);

  const handlePause = useCallback(() => {
    window.speechSynthesis.pause();
    setIsPaused(true);
    setIsPlaying(false);
  }, []);

  const handleStop = useCallback(() => {
    window.speechSynthesis.cancel();
    setIsPlaying(false);
    setIsPaused(false);
  }, []);

  // Autoplay on mount
  useEffect(() => {
    if (autoplay && text && window.speechSynthesis) {
      const timer = setTimeout(() => {
        handlePlay();
      }, 500);
      return () => clearTimeout(timer);
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(139,92,246,0.2)' : 'rgba(99,102,241,0.15)'}`,
        background: isDark
          ? 'linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08), rgba(236,72,153,0.05))'
          : 'linear-gradient(135deg, rgba(99,102,241,0.06), rgba(139,92,246,0.06), rgba(236,72,153,0.04))',
        backdropFilter: 'blur(12px)',
        height: '100%',
        position: 'relative',
        overflow: 'hidden',
        transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: isDark
            ? '0 8px 32px rgba(139,92,246,0.15)'
            : '0 8px 32px rgba(99,102,241,0.1)',
          borderColor: isDark ? 'rgba(139,92,246,0.3)' : 'rgba(99,102,241,0.25)',
        },
      }}
    >
      {/* Decorative gradient overlay */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          right: 0,
          width: 120,
          height: 120,
          borderRadius: '50%',
          background: isDark
            ? 'radial-gradient(circle, rgba(139,92,246,0.12), transparent 70%)'
            : 'radial-gradient(circle, rgba(99,102,241,0.08), transparent 70%)',
          transform: 'translate(30%, -30%)',
          pointerEvents: 'none',
        }}
      />

      <CardContent sx={{ p: 3, position: 'relative' }}>
        {/* Header with controls */}
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 1 }}>
          <Typography
            variant="subtitle2"
            sx={{
              fontWeight: 700,
              fontSize: '0.75rem',
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              color: isDark ? 'rgba(139,92,246,0.9)' : 'rgba(99,102,241,0.9)',
            }}
          >
            🎙 Narration
          </Typography>

          <WaveBars active={isPlaying} isDark={isDark} />

          <Box sx={{ ml: 'auto', display: 'flex', gap: 0.5 }}>
            {!isPlaying ? (
              <IconButton
                onClick={handlePlay}
                size="small"
                sx={{
                  color: isDark ? '#a78bfa' : '#6366f1',
                  border: `1px solid ${isDark ? 'rgba(139,92,246,0.3)' : 'rgba(99,102,241,0.2)'}`,
                  borderRadius: 2,
                  '&:hover': {
                    backgroundColor: isDark ? 'rgba(139,92,246,0.15)' : 'rgba(99,102,241,0.1)',
                  },
                }}
              >
                <VolumeUpIcon fontSize="small" />
              </IconButton>
            ) : (
              <IconButton
                onClick={handlePause}
                size="small"
                sx={{
                  color: isDark ? '#a78bfa' : '#6366f1',
                  border: `1px solid ${isDark ? 'rgba(139,92,246,0.3)' : 'rgba(99,102,241,0.2)'}`,
                  borderRadius: 2,
                  '&:hover': {
                    backgroundColor: isDark ? 'rgba(139,92,246,0.15)' : 'rgba(99,102,241,0.1)',
                  },
                }}
              >
                <PauseIcon fontSize="small" />
              </IconButton>
            )}
            {(isPlaying || isPaused) && (
              <IconButton
                onClick={handleStop}
                size="small"
                sx={{
                  color: isDark ? '#f87171' : '#ef4444',
                  border: `1px solid ${isDark ? 'rgba(248,113,113,0.3)' : 'rgba(239,68,68,0.2)'}`,
                  borderRadius: 2,
                  '&:hover': {
                    backgroundColor: isDark ? 'rgba(248,113,113,0.15)' : 'rgba(239,68,68,0.1)',
                  },
                }}
              >
                <StopIcon fontSize="small" />
              </IconButton>
            )}
          </Box>
        </Box>

        {/* Narration text */}
        <Typography
          variant="body1"
          sx={{
            fontSize: '0.95rem',
            lineHeight: 1.8,
            color: 'text.primary',
            fontStyle: 'italic',
            position: 'relative',
            pl: 2,
            borderLeft: `3px solid ${isDark ? 'rgba(139,92,246,0.4)' : 'rgba(99,102,241,0.3)'}`,
          }}
        >
          {text}
        </Typography>
      </CardContent>
    </Card>
  );
};
