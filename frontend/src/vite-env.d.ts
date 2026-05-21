/// <reference types="vite/client" />

declare global {
  interface Window {
    __HOLYSHEET_SPEC__?: import('./types').ReportSpec;
  }
}

export {};
