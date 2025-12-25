# Vercel serverless functions
# 
# IMPORTANT: All handlers in this package are FUNCTION-based handlers.
# They do NOT subclass BaseHTTPRequestHandler - they are simple functions
# that take a request dict and return a response dict.
#
# This prevents the issubclass() error that occurs when Vercel's runtime
# tries to check if handlers are class-based (BaseHTTPRequestHandler subclasses).

