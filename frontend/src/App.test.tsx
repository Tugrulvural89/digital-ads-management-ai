import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';
import { test, describe } from '@jest/globals';



// write test sample for typescript react

describe('App component', () => {
  test('renders the App component', () => {
    render(<App />);
    
    // Check if a specific element is in the document
    const linkElement = screen.getByText(/learn react/i);
    expect(linkElement).toBeInTheDocument();
  });

  test('should display the title in the header', () => {
    render(<App />);
    
    const titleElement = screen.getByText(/Welcome to My App/i);
    expect(titleElement).toBeInTheDocument();
  });
});

