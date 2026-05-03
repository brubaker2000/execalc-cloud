import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const body = await req.text();

    const upstream = await fetch("http://127.0.0.1:5000/orchestration/run", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": req.headers.get("x-user-id") ?? "",
        "X-Role": req.headers.get("x-role") ?? "",
        "X-Tenant-Id": req.headers.get("x-tenant-id") ?? "",
      },
      body,
      cache: "no-store",
    });

    const text = await upstream.text();

    return new NextResponse(text, {
      status: upstream.status,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    return NextResponse.json(
      {
        ok: false,
        error: error instanceof Error ? error.message : "proxy_error",
      },
      { status: 500 }
    );
  }
}
