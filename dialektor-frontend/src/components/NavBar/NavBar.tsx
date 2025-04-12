// import { NavLink } from '@mantine/core';
import { NavLink } from '@mantine/core';
import Icon from '@mui/material/Icon';
import HomeIcon from '@mui/icons-material/Home';

const NavBar = () => {
    return (
        <>
            <NavLink
                href="#required-for-focus"
                label="With icon"
                leftSection={<Icon component={HomeIcon}/>}
            />
        </>
    )
}

export default NavBar