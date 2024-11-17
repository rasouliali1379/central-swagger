import React, { useState } from 'react';
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';
import { API_LIST } from '../config';
import { AppBar, Toolbar, Typography, Select, MenuItem, FormControl } from '@mui/material';
const MultiSwagger = () => {
  const [selectedApi, setSelectedApi] = useState(API_LIST[0].url);

  const handleChange = (event) => {
    setSelectedApi(event.target.value);
  };

  return (
    <div>
      <AppBar position="static" sx={{ bgcolor: '#6ab42d' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Central Swagger
          </Typography>
          <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
            <Select
              value={selectedApi}
              onChange={handleChange}
              variant="outlined"
              sx={{
                backgroundColor: 'white',
                minWidth: 150,
              }}
            >
              {API_LIST.map((api) => (
                <MenuItem key={api.name} value={api.url}>
                  {api.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>



        </Toolbar>
      </AppBar>
      <div style={{ marginTop: '20px' }}>
        <SwaggerUI url={selectedApi} />
      </div>
    </div>
  );
};

export default MultiSwagger;