#!/bin/bash

# Stop PM2 processes
echo "Stopping C-3PO services..."
pm2 stop c3po-backend
pm2 stop c3po-frontend

# Delete PM2 processes
pm2 delete c3po-backend
pm2 delete c3po-frontend

echo "C-3PO has been stopped."
