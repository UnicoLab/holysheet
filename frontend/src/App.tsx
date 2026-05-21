import React from 'react';
import Container from '@mui/material/Container';
import { Layout } from './components/Layout';
import { BlockRenderer } from './registry';
import type { ReportSpec } from './types';

interface AppProps {
  spec: ReportSpec;
}

const App: React.FC<AppProps> = ({ spec }) => {
  return (
    <Layout spec={spec}>
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <BlockRenderer blocks={spec.blocks} />
      </Container>
    </Layout>
  );
};

export default App;
