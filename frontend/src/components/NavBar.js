import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';

export default function NavBar() {
  const navigate = useNavigate();
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          MP3 Converter
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            color="inherit"
            onClick={() => navigate('/upload')}
            sx={{ backgroundColor: isActive('/upload') ? 'rgba(255,255,255,0.1)' : 'transparent' }}
          >
            Upload
          </Button>
          <Button
            color="inherit"
            onClick={() => navigate('/download')}
            sx={{ backgroundColor: isActive('/download') ? 'rgba(255,255,255,0.1)' : 'transparent' }}
          >
            Download
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}