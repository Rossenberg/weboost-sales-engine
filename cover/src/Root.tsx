import React from "react";
import { Still } from "remotion";
import { Cover } from "./Cover";

export const Root: React.FC = () => (
  <>
    <Still id="Cover" component={Cover} width={1600} height={1200} defaultProps={{ wide: false }} />
    <Still id="CoverWide" component={Cover} width={1920} height={1080} defaultProps={{ wide: true }} />
  </>
);
