import React, { Component, type ReactNode } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';

// ─── Error Boundary ───────────────────────────────────────────────────────────

interface ErrorBoundaryProps {
  children: ReactNode;
  blockId?: string;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error(`[HolySheet] Error rendering block${this.props.blockId ? ` "${this.props.blockId}"` : ''}:`, error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <Paper
          sx={{
            p: 3,
            textAlign: 'center',
            borderColor: 'error.main',
            bgcolor: 'rgba(248, 113, 113, 0.05)',
          }}
        >
          <Box sx={{ fontSize: 32, mb: 1 }}>⚠️</Box>
          <Typography variant="h6" sx={{ mb: 0.5, color: 'error.main' }}>
            Rendering Error
          </Typography>
          {this.props.blockId && (
            <Typography variant="caption" sx={{ display: 'block', mb: 1, color: 'text.secondary' }}>
              Block: {this.props.blockId}
            </Typography>
          )}
          <Typography variant="body2" sx={{ color: 'text.secondary' }}>
            {this.state.error?.message || 'An unexpected error occurred.'}
          </Typography>
        </Paper>
      );
    }

    return this.props.children;
  }
}
