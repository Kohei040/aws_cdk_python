import React from 'react';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import styles from './Main.css';

export default function Main() {
  return(
    <React.Fragment>
      <Container className={styles.test}>
          SampleBody
      </Container>
      <Button className={styles.button}>
        Button
      </Button>
    </React.Fragment>
  );
}
