import React, { useMemo, useState } from 'react';
import Card from '@mui/material/Card';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckIcon from '@mui/icons-material/Check';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Syntax Highlighting ──────────────────────────────────────────────────────

/**
 * Simple syntax highlighting via regex.
 * Highlights: keywords, strings, comments, numbers, functions.
 */
function highlightCode(code: string, _language?: string): string {
  let html = code
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // Comments (single-line)
  html = html.replace(
    /((?:\/\/|#).*$)/gm,
    '<span style="color:#6b7280;font-style:italic">$1</span>'
  );

  // Multi-line comments
  html = html.replace(
    /(\/\*[\s\S]*?\*\/)/g,
    '<span style="color:#6b7280;font-style:italic">$1</span>'
  );

  // Strings (double and single quoted)
  html = html.replace(
    /(&quot;[^&]*?&quot;|"[^"]*?"|'[^']*?'|`[^`]*?`)/g,
    '<span style="color:#34d399">$1</span>'
  );

  // Numbers
  html = html.replace(
    /\b(\d+\.?\d*)\b/g,
    '<span style="color:#fbbf24">$1</span>'
  );

  // Keywords
  const keywords = 'import|export|from|const|let|var|function|return|if|else|for|while|class|interface|type|def|print|async|await|try|catch|finally|throw|new|this|super|extends|implements|static|public|private|protected|yield|of|in|switch|case|break|continue|default|do|void|null|undefined|true|false|None|True|False|self|lambda|with|as|raise|except|pass';
  html = html.replace(
    new RegExp(`\\b(${keywords})\\b`, 'g'),
    '<span style="color:#c084fc;font-weight:600">$1</span>'
  );

  // Function calls
  html = html.replace(
    /\b([a-zA-Z_]\w*)(?=\()/g,
    '<span style="color:#38bdf8">$1</span>'
  );

  return html;
}

// ─── Code Block Component ─────────────────────────────────────────────────────

export const CodeBlockComponent: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { code, language, title } = block.props;
  const isDark = theme.palette.mode === 'dark';
  const [copied, setCopied] = useState(false);

  const highlighted = useMemo(
    () => highlightCode(code || '', language),
    [code, language]
  );

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code || '');
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // fallback — silently ignore
    }
  };

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
        overflow: 'hidden',
      }}
    >
      {/* Header bar */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          px: 3,
          py: 1.5,
          borderBottom: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)'}`,
          backgroundColor: isDark ? 'rgba(0,0,0,0.3)' : 'rgba(0,0,0,0.03)',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          {/* Traffic light dots */}
          <Box sx={{ display: 'flex', gap: 0.75 }}>
            <Box sx={{ width: 10, height: 10, borderRadius: '50%', bgcolor: '#f43f5e' }} />
            <Box sx={{ width: 10, height: 10, borderRadius: '50%', bgcolor: '#fbbf24' }} />
            <Box sx={{ width: 10, height: 10, borderRadius: '50%', bgcolor: '#34d399' }} />
          </Box>
          <Typography
            variant="caption"
            sx={{ color: 'text.secondary', fontWeight: 600, fontSize: '0.75rem' }}
          >
            {title || language || 'Code'}
          </Typography>
        </Box>
        <IconButton size="small" onClick={handleCopy} sx={{ color: 'text.secondary' }}>
          {copied ? <CheckIcon sx={{ fontSize: 16 }} /> : <ContentCopyIcon sx={{ fontSize: 16 }} />}
        </IconButton>
      </Box>

      {/* Code content */}
      <Box
        sx={{
          p: 3,
          backgroundColor: isDark ? 'rgba(0,0,0,0.4)' : '#1e1e2e',
          overflow: 'auto',
          maxHeight: 500,
        }}
      >
        <pre
          style={{
            margin: 0,
            fontFamily: '"JetBrains Mono", "Fira Code", "Cascadia Code", Consolas, monospace',
            fontSize: '0.82rem',
            lineHeight: 1.7,
            color: '#e2e8f0',
            whiteSpace: 'pre',
            overflowX: 'auto',
          }}
        >
          <code dangerouslySetInnerHTML={{ __html: highlighted }} />
        </pre>
      </Box>
    </Card>
  );
};
