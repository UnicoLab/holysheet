import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockSpec } from '../types';

interface MarkdownBlockProps {
  block: BlockSpec;
  index: number;
}

/**
 * Simple markdown-to-HTML converter.
 * Handles: headings, bold, italic, code blocks, inline code, links, lists, paragraphs, hr.
 */
function simpleMarkdownToHtml(md: string): string {
  let html = md;

  // Code blocks (fenced)
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_match, _lang, code) => {
    return `<pre style="background:rgba(99,102,241,0.08);border-radius:8px;padding:16px;overflow-x:auto;font-size:13px;line-height:1.6"><code>${code.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</code></pre>`;
  });

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code style="background:rgba(99,102,241,0.1);padding:2px 6px;border-radius:4px;font-size:0.9em">$1</code>');

  // Headings
  html = html.replace(/^#### (.+)$/gm, '<h4 style="margin:20px 0 8px;font-weight:600;font-size:1rem">$1</h4>');
  html = html.replace(/^### (.+)$/gm, '<h3 style="margin:24px 0 10px;font-weight:600;font-size:1.1rem">$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2 style="margin:28px 0 12px;font-weight:700;font-size:1.25rem">$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1 style="margin:32px 0 14px;font-weight:700;font-size:1.5rem">$1</h1>');

  // Horizontal rules
  html = html.replace(/^---$/gm, '<hr style="border:none;border-top:1px solid rgba(128,128,128,0.2);margin:24px 0" />');

  // Bold & italic
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" style="color:#6366f1;text-decoration:none" target="_blank" rel="noopener">$1</a>');

  // Unordered lists
  html = html.replace(/^[\s]*[-*] (.+)$/gm, '<li style="margin:4px 0;line-height:1.6">$1</li>');
  html = html.replace(/(<li[^>]*>.*<\/li>\n?)+/g, (match) => `<ul style="padding-left:20px;margin:12px 0">${match}</ul>`);

  // Ordered lists
  html = html.replace(/^\d+\. (.+)$/gm, '<li style="margin:4px 0;line-height:1.6">$1</li>');

  // Paragraphs - wrap remaining text blocks
  html = html.replace(/^(?!<[a-z]|$)(.+)$/gm, '<p style="margin:8px 0;line-height:1.7">$1</p>');

  // Clean up double line breaks
  html = html.replace(/\n{2,}/g, '\n');

  return html;
}

export const MarkdownBlock: React.FC<MarkdownBlockProps> = ({ block }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const { content } = block.props;

  if (!content) {
    return null;
  }

  const htmlContent = simpleMarkdownToHtml(content);

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box
          sx={{
            '& h1:first-of-type, & h2:first-of-type': { marginTop: 0 },
            color: 'text.primary',
            fontSize: 14,
            lineHeight: 1.7,
          }}
          dangerouslySetInnerHTML={{ __html: htmlContent }}
        />
      </CardContent>
    </Card>
  );
};
