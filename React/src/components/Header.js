import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import styles from './Header.css';

export default function Header() {
  return(
    <React.Fragment>
      <AppBar potion='static' color='default'>
        <Toolbar>
          <Typography variant='h6' color='inherit'>
            SampleApp
          </Typography>
          <Button>FEATURE</Button>
          <Button>TEST</Button>
        </Toolbar>
      </AppBar>
    </React.Fragment>
  );
}
