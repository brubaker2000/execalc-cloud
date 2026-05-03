import { NextRequest, NextResponse } from "next/server";

type RouteContext = {
  params: Promise<{
    envelopeId: string;
  }>;
};

export async function GET(req: NextRequest, context: RouteContext) {
  try {
    const { envelopeId } = await context.params;

    const upstream = await fetch(
      `http://127.0.0.1:5000/decision/${encodeURIComponent(envelopeId)}`,
      {
        method: "GET",
        headers: {
          "X-User-Id": req.headers.get("x-user-id") ?? "",
          "X-Role": req.headers.get("x-role") ?? "",
          "X-Tenant-Id": req.headers.get("x-tenant-id") ?? "",
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
