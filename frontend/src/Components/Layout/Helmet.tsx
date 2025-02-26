import { Stack } from "@mui/material";
import React from "react";
import Header from "./Header";

function Helmet({
  children,
  title,
}: {
  children: React.ReactNode;
  title: string | undefined;
}) {
  return (
      <Stack
      spacing={5}
      direction="column"
      justifyContent={"flex-start"}
      alignItems="center"
      sx={{ width: "100%" }}
    >
      {title && (
        <Header />
      )}

      {children}
    </Stack>
  );
}

export default Helmet;
