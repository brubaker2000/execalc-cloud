import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const limit = searchParams.get("limit") || "10";

    const upstream = await fetch(
      `http://127.0.0.1:5000/decision/recent?limit=${encodeURIComponent(limit)}`,
      {
        method: "GET",
        headers: {
          "X-User-Id": req.headers.get("x-user-id") || "test_user",
          "X-Role": req.headers.get("x-role") || "operator",
          "X-Tenant-Id": req.headers.get("x-tenant-id") || "tenant_test_001",
        },
        cache: "no-store",
      }
    );

    const text = await upstream.text();

    return new NextResponse(text, {
      status: upstream.status,
      headers: {
        "Content-Type": "application/json",
      },
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
