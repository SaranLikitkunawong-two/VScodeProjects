import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import Nav from "@/components/Nav";
import "./globals.css";

const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: "Future Forward Planning — NDIS Plan Management",
  description:
    "Independent NDIS plan management for Australian participants. We pay your providers, keep your budget in plain view, and answer when you call.",
  openGraph: {
    title: "Future Forward Planning — NDIS Plan Management",
    description:
      "Independent NDIS plan management for Australian participants. Two-day invoice turnaround, real-time budgets, no cost to participants.",
    type: "website",
    locale: "en_AU",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en-AU" className={inter.variable}>
      <body>
        <Nav />
        {children}
        <Analytics />
      </body>
    </html>
  );
}
