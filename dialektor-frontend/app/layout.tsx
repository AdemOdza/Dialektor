import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Dialektor",
  description: "A website to show off how words are said/spelled in different dialects of the Albanian language",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
