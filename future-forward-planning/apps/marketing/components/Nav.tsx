"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ArrowIcon } from "./Icons";

function Brand() {
  return (
    <Link className="brand" href="/">
      <span className="brand-mark" aria-hidden></span>
      <span>Future Forward Planning</span>
    </Link>
  );
}

export default function Nav() {
  const pathname = usePathname();
  const isActive = (path: string) =>
    path === "/" ? pathname === "/" : pathname.startsWith(path);

  return (
    <header className="nav" role="banner">
      <div className="container nav-inner">
        <Brand />
        <nav className="nav-links" aria-label="Primary">
          <Link className={`nav-link ${isActive("/") ? "active" : ""}`} href="/">
            Home
          </Link>
          <Link className={`nav-link ${isActive("/news") ? "active" : ""}`} href="/news">
            News
          </Link>
          <Link className={`nav-link ${isActive("/signup") ? "active" : ""}`} href="/signup">
            Sign up
          </Link>
          <Link className="nav-link" href="/signup">
            Login
          </Link>
          <Link className="btn btn-primary nav-cta" href="/signup">
            Join the waitlist <ArrowIcon />
          </Link>
        </nav>
      </div>
    </header>
  );
}
