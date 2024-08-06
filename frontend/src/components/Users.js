import React, { useEffect, useState } from 'react';
import './Users.css';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isUpdate, setIsUpdate] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://localhost:5001/users/list');
      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }
      const data = await response.json();
      data.forEach(user => {
        user.nameNew = user.name
        user.emailNew = user.email
      });
      setUsers(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };
  const editUser = async (user) => {
    user.isUpdate = !user.isUpdate
    setIsUpdate(!isUpdate)

  };
  const cancelUser = async (user) => {
    user.isUpdate = !user.isUpdate
    user.nameNew = user.name
    user.emailNew = user.emailNew
    setIsUpdate(!isUpdate)

  };
  const handleInputChange = (event,user) => {
    const { name, value } = event.target;
    user[name] = value
    setIsUpdate(!isUpdate)
    console.log(event.target,user)
  };
  const saveUser = async (user) => {
   
    try {
      const response = await fetch(`http://localhost:5001/admin/update_user`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':`Bearer `+localStorage.getItem('authToken')
        },
        body: JSON.stringify({email:user.emailNew,id:user.id,name:user.nameNew}),
      });

      if (!response.ok) {
        throw new Error('Failed to delete user');
      }
      user.isUpdate = false
      user.email = user.emailNew
      user.name = user.nameNew
      setIsUpdate(!isUpdate)
    } catch (error) {
      setError(error.message);
    }
  };
  const deleteUser = async (userId) => {
    try {
      const response = await fetch(`http://localhost:5001/admin/delete_user`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':`Bearer `+localStorage.getItem('authToken')
        },
        body: JSON.stringify({id:userId}),
      });
      if (!response.ok) {
        throw new Error('Failed to delete user');
      }
      fetchUsers()
      // setUsers(users.filter(user => user.id !== userId));
    } catch (error) {
      setError(error.message);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="users">
      <h1>Users</h1>
      <table>
        <thead>
          <tr>
            <th>User ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td><div className='td-item-50'>{user.id}</div></td>
              <td>
                <div className='td-item-250'>{user.isUpdate?'':user.name} {user.isUpdate && <input type="text" name="nameNew" value={user.nameNew || ''}  onChange={e=>handleInputChange(e,user)}/>}</div></td>
              <td><div className='td-item-250'>{user.isUpdate?'':user.email} {user.isUpdate &&<input type="text" name="emailNew" value={user.emailNew || ''} onChange={e=>handleInputChange(e,user)} />}</div></td>
              <td >
                 <div className='Actions'> 
                  
                  { !user.isUpdate && <button onClick={() => editUser(user)}>Edit</button>}
                  { !user.isUpdate && <button onClick={() => deleteUser(user.id)}>Delete</button>}
                   {user.isUpdate &&  <button onClick={() => saveUser(user)}>Save</button>}
                   {user.isUpdate &&  <button onClick={() => cancelUser(user)}>Cancel</button>}
                 </div>
                {/* Add more actions like edit or view details if needed */}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Users;
