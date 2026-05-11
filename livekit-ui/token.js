const { AccessToken } = require("livekit-server-sdk");

async function generateToken() {
  const at = new AccessToken(
    "devkey",  // Must match LIVEKIT_API_KEY in agent .env
    "secret",  // Must match LIVEKIT_API_SECRET in agent .env
    {
      identity: "nivetha",
      ttl: "24h",  // Token valid for 24 hours
    }
  );

  at.addGrant({
    roomJoin: true,
    room: "test-room",
    canPublish: true,
    canSubscribe: true,
  });

  const token = await at.toJwt();
  console.log("✅ Your JWT Token (valid 24h):\n");
  console.log(token);
}

generateToken();
