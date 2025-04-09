/** @type {import('next').NextConfig} */
const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination:
          process.env.NODE_ENV === "development" || process.env.NODE_ENV === "production"
            ? `${process.env.NEXT_PUBLIC_API_BASE_URL}/:path*`
            : "/api/",
      },
      {
        source: "/docs",
        destination:
          process.env.NODE_ENV === "development"
            ? `${process.env.NEXT_PUBLIC_API_BASE_URL}/py/docs`
            : "/api/py/docs",
      },
      {
        source: "/openapi.json",
        destination:
          process.env.NODE_ENV === "development"
            ? `${process.env.NEXT_PUBLIC_API_BASE_URL}/py/openapi.json`
            : "/api/py/openapi.json",
      },
    ];
  },
};

module.exports = nextConfig;
