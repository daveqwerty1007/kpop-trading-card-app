import React, { useState, useEffect } from 'react';

const Filters = ({ onFilterChange, selectedFilters, filterOptions }) => {
  const [filters, setFilters] = useState(selectedFilters);

  useEffect(() => {
    setFilters(selectedFilters);
  }, [selectedFilters]);

  const handleChange = (filterType, value) => {
    const updatedFilters = {
      ...filters,
      [filterType]: value,
    };
    setFilters(updatedFilters);
    onFilterChange(filterType, value);
  };

  return (
    <div>
      <h2>Filters</h2>
      <select onChange={(e) => handleChange('artists', e.target.value)} value={filters.artists}>
        <option value="">Select Artist</option>
        {filterOptions.artists.map(artist => (
          <option key={artist} value={artist}>{artist}</option>
        ))}
      </select>
      <select onChange={(e) => handleChange('groups', e.target.value)} value={filters.groups}>
        <option value="">Select Group</option>
        {filterOptions.groups.map(group => (
          <option key={group} value={group}>{group}</option>
        ))}
      </select>
      <select onChange={(e) => handleChange('albums', e.target.value)} value={filters.albums}>
        <option value="">Select Album</option>
        {filterOptions.albums.map(album => (
          <option key={album} value={album}>{album}</option>
        ))}
      </select>
      <select onChange={(e) => handleChange('prices', e.target.value)} value={filters.prices}>
        <option value="">Select Price Range</option>
        {filterOptions.prices.map(price => (
          <option key={price} value={price}>{price}</option>
        ))}
      </select>
    </div>
  );
};

export default Filters;
