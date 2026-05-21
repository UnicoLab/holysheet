import React, { useState, useEffect, useCallback, useRef } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import CloseIcon from '@mui/icons-material/Close';
import InstallDesktopOutlinedIcon from '@mui/icons-material/InstallDesktopOutlined';
import { alpha, useTheme } from '@mui/material/styles';
import { motion, AnimatePresence } from 'framer-motion';

// ─── PWA Install Component ────────────────────────────────────────────────────
//
// Shows a floating install banner when:
//  1. features.pwa_mode is true (controlled by parent)
//  2. The browser fires the `beforeinstallprompt` event
//
// The actual service worker & manifest injection is handled by Python exporters.

interface BeforeInstallPromptEvent extends Event {
  prompt(): Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export const PWAInstall: React.FC = () => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [dismissed, setDismissed] = useState(false);
  const [installed, setInstalled] = useState(false);
  const promptRef = useRef<BeforeInstallPromptEvent | null>(null);

  useEffect(() => {
    // Check if already dismissed in this session
    try {
      if (sessionStorage.getItem('holysheet_pwa_dismissed') === '1') {
        setDismissed(true);
      }
    } catch {
      // ignore
    }

    const handleBeforeInstall = (e: Event) => {
      e.preventDefault();
      const evt = e as BeforeInstallPromptEvent;
      promptRef.current = evt;
      setDeferredPrompt(evt);
    };

    const handleAppInstalled = () => {
      setInstalled(true);
      setDeferredPrompt(null);
      promptRef.current = null;
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstall);
    window.addEventListener('appinstalled', handleAppInstalled);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstall);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const handleInstall = useCallback(async () => {
    const prompt = promptRef.current;
    if (!prompt) return;

    await prompt.prompt();
    const choice = await prompt.userChoice;
    if (choice.outcome === 'accepted') {
      setInstalled(true);
    }
    setDeferredPrompt(null);
    promptRef.current = null;
  }, []);

  const handleDismiss = useCallback(() => {
    setDismissed(true);
    try {
      sessionStorage.setItem('holysheet_pwa_dismissed', '1');
    } catch {
      // ignore
    }
  }, []);

  // Don't show if no prompt available, already dismissed, or already installed
  if (!deferredPrompt || dismissed || installed) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 20, scale: 0.95 }}
        transition={{ duration: 0.3, ease: 'easeOut' }}
        style={{
          position: 'fixed',
          bottom: 88, // above the nav FAB if present
          left: 24,
          zIndex: theme.zIndex.snackbar,
        }}
        className="no-print"
      >
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 1.5,
            px: 2,
            py: 1.5,
            borderRadius: 3,
            backgroundColor: isDark
              ? alpha(theme.palette.background.paper, 0.92)
              : alpha(theme.palette.background.paper, 0.96),
            backdropFilter: 'blur(16px)',
            border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
            boxShadow: `0 8px 32px ${alpha(theme.palette.common.black, isDark ? 0.4 : 0.15)}`,
            maxWidth: 340,
          }}
        >
          <InstallDesktopOutlinedIcon
            sx={{
              color: theme.palette.primary.main,
              fontSize: 28,
            }}
          />
          <Box sx={{ flex: 1, minWidth: 0 }}>
            <Typography variant="body2" sx={{ fontWeight: 600, fontSize: '0.85rem', lineHeight: 1.3 }}>
              Install Dashboard
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.72rem' }}>
              Add to home screen for offline access
            </Typography>
          </Box>
          <Button
            variant="contained"
            size="small"
            onClick={handleInstall}
            sx={{
              textTransform: 'none',
              fontWeight: 600,
              fontSize: '0.75rem',
              borderRadius: 2,
              px: 2,
              minWidth: 'auto',
              boxShadow: 'none',
              '&:hover': { boxShadow: 'none' },
            }}
          >
            Install
          </Button>
          <IconButton
            size="small"
            onClick={handleDismiss}
            sx={{ color: 'text.secondary', ml: -0.5 }}
          >
            <CloseIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Box>
      </motion.div>
    </AnimatePresence>
  );
};
