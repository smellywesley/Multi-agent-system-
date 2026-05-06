import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Biomedical Research Intelligence",
  description: "Premium multi-agent research synthesis interface"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
