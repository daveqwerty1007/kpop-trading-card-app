import React from 'react';

function AdminPanel() {
  return (
    <div>
      <h1>Admin Panel</h1>
      <p>Manage the inventory, users, and orders from this panel.</p>
      <a href="/admin/manage_inventory">Manage Inventory</a>
      <a href="/admin/manage_users">Manage Users</a>
      <a href="/admin/manage_orders">Manage Orders</a>
    </div>
  );
}

export default AdminPanel;
