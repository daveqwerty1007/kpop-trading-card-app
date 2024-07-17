import React from 'react';

const Filters = () => {
  return (
    <div>
      <h2>Filters</h2>
      <select>
        <option value="group">Group</option>
        {/* Add more options */}
      </select>
      <select>
        <option value="member">Member</option>
        {/* Add more options */}
      </select>
    </div>
  );
};

export default Filters;