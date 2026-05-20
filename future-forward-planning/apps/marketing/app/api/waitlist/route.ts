import { NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

const ROLES = ["participant", "family", "support_coordinator", "provider", "other"] as const;
type Role = (typeof ROLES)[number];

type Payload = {
  firstName?: string;
  email?: string;
  phone?: string | null;
  role?: string;
};

export async function POST(req: Request) {
  let body: Payload;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid request body." }, { status: 400 });
  }

  const firstName = (body.firstName || "").trim();
  const email = (body.email || "").trim().toLowerCase();
  const phone = body.phone ? body.phone.toString().trim() : null;
  const role = body.role as Role | undefined;

  if (!firstName) return NextResponse.json({ error: "First name is required." }, { status: 400 });
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
    return NextResponse.json({ error: "A valid email is required." }, { status: 400 });
  if (phone && !/^[\d\s+()-]{6,}$/.test(phone))
    return NextResponse.json({ error: "Phone number format is invalid." }, { status: 400 });
  if (!role || !ROLES.includes(role))
    return NextResponse.json({ error: "Please select which best describes you." }, { status: 400 });

  const { error } = await supabase
    .from("waitlist")
    .insert({ first_name: firstName, email, phone, role });

  if (error) {
    if (error.code === "23505") {
      return NextResponse.json({ success: true });
    }
    console.error("waitlist insert error", error);
    return NextResponse.json({ error: "Could not save your details. Please try again." }, { status: 500 });
  }

  return NextResponse.json({ success: true }, { status: 201 });
}
