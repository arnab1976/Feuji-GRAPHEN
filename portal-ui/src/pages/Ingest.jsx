const Ingest = () => {
  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', backgroundColor: '#990000', color: 'white', textAlign: 'center', padding: '50px' }}>
      <h1 style={{ fontSize: '50px', fontWeight: 'bold', marginBottom: '20px' }}>STOP! YOU ARE ON THE WRONG PAGE</h1>
      <p style={{ fontSize: '24px' }}>This is the old, hardcoded React prototype running on port 5173.</p>
      <p style={{ fontSize: '24px', fontWeight: 'bold', marginTop: '20px' }}>Please open a NEW browser tab and go to: <a href="http://127.0.0.1:8004" style={{ color: '#ffff00', textDecoration: 'underline' }}>http://127.0.0.1:8004</a></p>
      <p style={{ fontSize: '20px', marginTop: '40px' }}>The real portal (index.html) is served by FastAPI on port 8004. It has the fully functional upload button and is not hardcoded.</p>
    </div>
  );
};

export default Ingest;
