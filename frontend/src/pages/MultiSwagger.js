import React, {useEffect, useState} from 'react';
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';
import {AppBar, FormControl, MenuItem, Select, Toolbar, Typography} from '@mui/material';

const MultiSwagger = () => {
    const [apiList, setApiList] = useState([]);
    const [selectedSpec, setSelectedSpec] = useState(null);

    useEffect(() => {
        const loadApiList = async () => {
            try {
                const response = await fetch(process.env.REACT_APP_API_LIST_URL);
                const data = await response.json();
                setApiList(data.items);
                if (data.items.length > 0) {
                    setSelectedSpec(data.items[0].spec);
                }
            } catch (error) {
                console.error('Failed to fetch API list:', error);
            }
        };

        loadApiList();
    }, []);

    const handleChange = (event) => {
        const selectedApi = apiList.find((api) => api.name === event.target.value);
        setSelectedSpec(selectedApi?.spec || null);
    };

    return (
        <div>
            <AppBar position="static" sx={{bgcolor: '#6ab42d'}}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{flexGrow: 1}}>
                        Central Swagger
                    </Typography>
                    <FormControl sx={{m: 1, minWidth: 120}} size="small">
                        <Select
                            value={selectedSpec ? apiList.find((api) => api.spec === selectedSpec)?.name : ''}
                            onChange={handleChange}
                            variant="outlined"
                            sx={{
                                backgroundColor: 'white',
                                minWidth: 150,
                            }}
                        >
                            {apiList.map((api) => (
                                <MenuItem key={api.name} value={api.name}>
                                    {api.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Toolbar>
            </AppBar>
            <div style={{marginTop: '20px'}}>
                {selectedSpec && <SwaggerUI spec={selectedSpec}/>}
            </div>
        </div>
    );
};

export default MultiSwagger;