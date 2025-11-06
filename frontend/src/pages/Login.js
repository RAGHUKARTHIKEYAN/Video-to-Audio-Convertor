import React from 'react';
import { Navigate } from 'react-router-dom';

// The login page was removed; redirect any attempts to /login to /signup
export default function Login() {
  return <Navigate to="/signup" replace />;
}