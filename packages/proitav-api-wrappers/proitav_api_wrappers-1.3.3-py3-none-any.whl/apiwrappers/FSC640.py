"""API Wrapper for FSC640

Firmware version 1.0.9
"""

import logging
import telnetlib
import socket

logger = logging.getLogger(__name__)


class FSC640_Device:
    def __init__(
        self,
        ip: str,
        port: int = 24,
        timeout: int = 2,
        debug: bool = False,
        verbose: bool = True,
    ):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.debug = debug
        self.tn = None
        self.verbose = verbose

    def connect(self, max_attempts=3) -> bool:
        for attempt in range(max_attempts):
            if self.tn is None:
                try:
                    self.tn = telnetlib.Telnet(self.ip, self.port, timeout=self.timeout)
                    if self.debug:
                        self.tn.set_debuglevel(1)
                    self.tn.read_until(b"~ # ", timeout=self.timeout)
                    print(f"Connected to {self.ip}")
                    return True
                except (socket.timeout, EOFError) as e:
                    self.tn = None
                    if attempt == max_attempts - 1:
                        raise TimeoutError(
                            f"Connection to {self.ip} failed after {max_attempts} attempts"
                        ) from e
                    print(f"Connection attempt {attempt + 1} failed, retrying...")
            else:
                return True
        return False

    def send(self, message):
        try:
            if not self.connect():
                return "Failed to connect"
        except TimeoutError as e:
            print(f"Error connecting to {self.ip}: {e}")
            return "Failed to connect"

        try:
            if self.verbose:
                print(f"Sending command: {message}")
            self.tn.write(message.encode("ascii") + b"\r\n")
            response = self.tn.read_until(b"~ # ")

            # Clean up the response
            cleaned_response = response.decode("ascii").strip()
            lines = cleaned_response.split("\n")
            # Remove the echoed command (first two lines) and the prompt
            cleaned_lines = [line.strip() for line in lines[2:-1] if line.strip()]
            finished_response = "\n".join(cleaned_lines)
            if self.verbose:
                print(f"Received response: {finished_response}")
            return finished_response

        except Exception as e:
            print(f"Error sending command to {self.ip}: {e}")
            return "Failed to send command"

    def close(self):
        if self.tn is not None:
            self.tn.close()
            self.tn = None
            if self.verbose:
                print(f"Closed connection to {self.ip}")

    def set_name(self, name: str) -> str:
        # Validate name length
        if not 1 <= len(name) <= 20:
            return "Error: Name must be 1-20 characters long"

        # Validate name characters
        allowed_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-"
        )
        if not set(name).issubset(allowed_chars):
            return "Error: Name can only contain letters, numbers, spaces, '_', and '-'"

        # If validation passes, send the command
        return self.send(f"gbconfig --name {name}")

    def get_name(self) -> str:
        return self.send("gbconfig -s name")

    def get_device_info(self) -> dict:
        """Returns a dictionary with the model and firmware version"""
        response = self.send("gbconfig -s device-info")
        lines = response.split("\n")
        if len(lines) >= 2:
            return {"model": lines[0].strip(), "firmware_version": lines[1].strip()}
        else:
            return {"model": "Unknown", "firmware_version": "Unknown"}

    def reboot(self):
        """Reboots the device"""
        self.send("gbcontrol --reboot")

    def factory_reset(self):
        """Factory resets the device"""
        self.send("gbcontrol --reset-to-default")

    def set_output_resolution(self, resolution: str = "Auto"):
        """Sets the output resolution
        Valid resolutions: Auto, 3840x2160P@60, 3840x2160P@50, 3840x2160P@30, 3840x2160P@25, 3840x2160P@24,
        1920x1080P@60, 1920x1080P@50, 1920x1080P@30, 1920x1080P@25, 1920x1080P@24, 1680x1050P@60,
        1600x1200P@60, 1440x900P@60, 1366x768P@60, 1280x1024P@60, 1280x720P@60, 1280x720P@50,
        1024x768P@60, 800x600P@60, 720x480P@60, 640x480P@60
        """
        valid_resolutions = {
            "Auto",
            "3840x2160P@60",
            "3840x2160P@50",
            "3840x2160P@30",
            "3840x2160P@25",
            "3840x2160P@24",
            "1920x1080P@60",
            "1920x1080P@50",
            "1920x1080P@30",
            "1920x1080P@25",
            "1920x1080P@24",
            "1680x1050P@60",
            "1600x1200P@60",
            "1440x900P@60",
            "1366x768P@60",
            "1280x1024P@60",
            "1280x720P@60",
            "1280x720P@50",
            "1024x768P@60",
            "800x600P@60",
            "720x480P@60",
            "640x480P@60",
        }

        if resolution not in valid_resolutions:
            return f"Error: Invalid resolution. Valid resolutions are: {', '.join(sorted(valid_resolutions))}"

        return self.send(f"gbconfig --output-resolution {resolution}")

    def get_output_resolution(self) -> str:
        """Returns the current output resolution"""
        return self.send("gbconfig -s output-resolution")

    def set_hdcp_enabled(self, mode: str = "n"):
        """Sets the HDCP mode
        Valid modes: y, n
        """
        if mode not in ["y", "n"]:
            return "Error: Invalid mode. Valid modes are: y, n"
        return self.send(f"gbconfig --hdcp-enable {mode}")

    def get_hdcp_enabled(self) -> str:
        """Returns the current HDCP mode"""
        return self.send("gbconfig -s hdcp-enable")

    def get_input_state(self, input: str = None) -> str:
        """Returns the current input state
        Valid inputs: hdmi, usbc, airplay1, miracast3
        """
        if input is None:
            return self.send("gbconfig -s input-video")
        else:
            return self.send(f"gbconfig -s input-video {input}")

    def set_auto_switching_enabled(self, mode: str = "y"):
        """Sets the auto switching mode
        Valid modes: y, n
        """
        self.send(f"gbconfig --auto-switch {mode}")

    def get_auto_switching(self) -> bool:
        """Returns True if auto switching is enabled, False otherwise"""
        response = self.send("gbconfig -s auto-switch")
        if response == "y":
            return True
        else:
            return False

    def set_multiview_enabled(self, mode: str = "y"):
        """Sets the multiview mode
        Valid modes: y, n
        """
        self.send(f"gbconfig --multiview {mode}")

    def get_multiview_enabled(self) -> bool:
        """Returns True if multiview is enabled, False otherwise"""
        response = self.send("gbconfig -s multiview")
        if response == "y":
            return True
        else:
            return False

    def start_video(self, video_name: str, win_no: int = None):
        """
        Start displaying a video source.

        Args:
            video_name (str): {hdmi, usbc, airplay1, miracast3, guide} The name of the video source or 'guide' for guide screen.
            win_no (int, optional): The window number for multiview layout (1 to max windows).

        Returns:
            str: The response from the device (empty string if successful).

        Examples:
            start_video("hdmi", 1)
            start_video("guide")
        """
        command = f"gblayout --start-video {video_name}"
        if win_no is not None:
            command += f" {win_no}"

        self.send(command)

    def stop_video(self, video_name: str = None, win_no: int = None):
        """
        Stop displaying a video source. If multiple video sources are playing,
        the video with the lowest window number will be stopped.

        Args:
            video_name (str): {hdmi, usbc, airplay1, miracast3, guide} The name of the video source or 'guide' for guide screen.

        Returns:
            str: The response from the device (empty string if successful).
        """

        command = "gblayout --stop-video 1"
        return self.send(command)

    def set_full_screen(self, video_name: str):
        """Sets the video source to full screen
        Valid video names: hdmi, usbc, airplay1, miracast3, guide
        """
        self.send(f"gbconfig --video-source {video_name}")

    def get_video_output_status(self) -> str:
        # BUG: The API is not working as expected - No Response
        """Returns the current video output status"""
        return self.send("gbconfig -s video-source")

    def set_usb_host_mode(self, mode: str = "auto"):
        """Sets the USB host mode
        Valid modes: auto, usbcin, usbhost, wireless
        """
        self.send(f"gbconfig --usb-host {mode}")

    def get_usb_host_mode(self) -> str:
        """Returns the current USB host mode"""
        return self.send("gbconfig -s usb-host-mode")

    def set_auto_standby(self, mode: str = "y"):
        """Sets the auto standby mode
        Valid modes: y, n
        """
        self.send(f"gbconfig --auto-standby {mode}")

    def get_auto_standby(self) -> bool:
        """Returns True if auto standby is enabled, False otherwise"""
        response = self.send("gbconfig -s auto-standby")
        if response == "y":
            return True
        else:
            return False

    def set_auto_standby_timeout(self, timeout: int = 120):
        """Sets the standby timeout
        Valid timeout: 0 to 3600 seconds
        Default timeout: 120 seconds
        """
        self.send(f"gbconfig --auto-standby-time {timeout}")

    def get_auto_standby_timeout(self) -> int:
        """Returns the current standby timeout"""
        return int(self.send("gbconfig -s auto-standby-time"))

    def set_cec_command(self, on_off: str, code: str):
        """Sets the CEC command
        Valid on_off: on, off
        Default on code: 4004
        Default off code: ff36
        """
        self.send(f"gbconfig --cec-cmd {on_off} {code}")

    def get_cec_command(self) -> dict:
        """Returns the current CEC commands for on and off states"""
        response = self.send("gbconfig -s cec-cmd")
        cec_commands = {"on": None, "off": None}

        for line in response.split("\n"):
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                state, code = parts
                if state in ["on", "off"]:
                    cec_commands[state] = code if code != "[Undefined]" else None

        return cec_commands

    def set_rs232_role(self, role: str = "com"):
        """Sets the RS232 role
        Valid roles:
            api : Receive the API commands sent by the external controller,
            com: Conventional communication, control the peripherals such as display, participate in standby related power on/off display operations,
            passthrough: Connect the RS232 port to the RS232 channel of the port so that the RS232 data is transparently transmitted between the local RS232 port and remote HDBT RX.
        Default role: com
        """
        self.send(f"gbconfig --rs232-role {role}")

    def get_rs232_role(self) -> str:
        """Returns the current RS232 role"""
        return self.send("gbconfig -s rs232-role")

    def set_rs232_settings(self, rs232_settings: str):
        """Sets the RS232 settings
        default: 115200-8n1
        """
        self.send(f"gbconfig --rs232-param {rs232_settings}")

    def get_rs232_settings(self) -> str:
        """Returns the current RS232 settings"""
        return self.send("gbconfig -s rs232-param")

    def set_rs232_baudrate(self, baudrate: int):
        """Sets the RS232 baudrate
        Valid baudrates: 9600, 19200, 38400, 57600, 115200
        """
        self.send(f"gbconfig --rs232-baudrate {baudrate}")

    def get_rs232_baudrate(self) -> int:
        """Returns the current RS232 baudrate"""
        return int(self.send("gbconfig -s rs232-baudrate"))

    def set_rs232_command(
        self, command_name: str, format_type: str = None, command: str = None
    ):
        """
        Sets or deletes an RS232 command.

        Args:
            command_name (str): The name of the command (e.g., 'on', 'off', or custom name).
            format_type (str, optional): The format of the command ('hex' or 'str'). If None, the command will be deleted.
            command (str, optional): The actual command string. Required if format_type is provided.

        Returns:
            str: The response from the device (empty string if successful).

        Examples:
            set_rs232_command("on", "str", "Power on")
            set_rs232_command("volumeup", "hex", "112233445566")
            set_rs232_command("custom_command")  # Deletes the command
        """
        if format_type is None and command is None:
            # Delete the command
            return self.send(f"gbconfig --rs232-cmd {command_name}")
        elif format_type is not None and command is not None:
            # Set the command
            if format_type not in ["hex", "str"]:
                raise ValueError("format_type must be either 'hex' or 'str'")
            return self.send(
                f'gbconfig --rs232-cmd "{command_name}" {format_type} "{command}"'
            )
        else:
            raise ValueError(
                "Both format_type and command must be provided to set a command"
            )

    def get_rs232_command(self, command_name: str = None) -> list:
        """
        Retrieves the RS232 command(s).

        Args:
            command_name (str, optional): The name of the command to retrieve. If None, retrieves all commands.

        Returns:
            list: A list of dictionaries, each containing 'name', 'type', and 'command' keys.
            If a specific command_name is provided, returns a list with only that command.

        Examples:
            get_rs232_command()  # Returns all commands
            get_rs232_command("on")  # Returns only the "on" command
        """
        response = self.send(
            "gbconfig -s rs232-cmd"
            if command_name is None
            else f'gbconfig -s rs232-cmd "{command_name}"'
        )
        commands = []
        for line in response.split("\n"):
            parts = line.strip().split(None, 2)
            if len(parts) == 3:
                name, cmd_type, command = parts
                commands.append(
                    {"name": name, "type": cmd_type, "command": command.strip('"')}
                )
        return commands

    def set_sinkpower_mode(self, mode: str = "cec"):
        """When the device enters or exits standby mode,
        in additions to powering on/off the display through CEC messages,
        the device also can send the corresponding commands through RS232 port.
        This API is used to configure whether to send RS232 command when powering on/off the display.

        Note: The actual activation of sending power on/off command through
        RS232 port requires three conditions to be met:
        - TheRS232portworkmodeiscom,namely,controlperipherals
        - TheRS232onoroffmessageisdefined
        - Thisconfigurationisboth
        As the factory default, this configuration is set cec, when the device enters or exits standby mode, the device sends [power on/off command through CEC messages only.

        Valid modes: cec, both
        """
        self.send(f"gbconfig --sinkpower-mode {mode}")

    def get_sinkpower_mode(self) -> str:
        """Returns the current sink power mode"""
        return self.send("gbconfig -s sinkpower-mode")

    def set_sinkpower(self, on_off: str):
        """
        Powers on or off the display.

        Args:
            on_off (str): {on, off} The state of the display.
        """
        self.send(f"gbconfig --sinkpower {on_off}")

    def get_sinkpower(self) -> str:
        """Returns the current sink power state"""
        return self.send("gbconfig -s sinkpower")

    def send_cec_or_rs232_command(self, command_name: str, send_method: str = None):
        """
        Sends a CEC or/and RS232 command to the device.

        Args:
            command_name (str): The name of the command to be sent.
            send_method (str, optional): The method to use for sending the command. Defaults to None.
                Valid options: rs232, cec, both. If None, the configuration of gbconfig --sinkpower-mode is used.
        """
        if send_method is None:
            send_method = self.get_sinkpower_mode()
        self.send(f"gbcontrol --send-cmd {command_name} {send_method}")

    def send_rs232_data(
        self,
        cmd_str: str,
        rs232_settings: str = "9600-8n1",
        add_carriage_return: str = "off",
        hex_format: str = "off",
        timeout: int = 0,
        response_size: int = 0,
    ) -> str:
        """
        Sends data through the RS232 port and receives the response data.

        Args:
            cmd_str (str): The data to be sent.
            rs232_settings (str, optional): The RS232 port settings. Defaults to "9600-8n1".
            add_carriage_return (str, optional): Whether to add a carriage return at the end of the data. Defaults to "off".
            hex_format (str, optional): Whether the cmd_str is in hexadecimal format. Defaults to "off".
            timeout (int, optional): The timeout in milliseconds. Defaults to 0.
            response_size (int, optional): The size of the response data to be received. Defaults to 0.

        Returns:
            str: The response data received.
        """
        command = "gbcontrol --serial"
        if rs232_settings:
            command += f" -b {rs232_settings}"
        if add_carriage_return:
            command += f" -r {add_carriage_return}"
        if hex_format:
            command += f" -h {hex_format}"
        if timeout:
            command += f" -t {timeout}"
        command += f" {cmd_str}"
        response = self.send(command)
        return response

    def set_network_isolation_enabled(self, mode: str = "n"):
        """
        Sets the network isolation mode
        Valid modes: y, n
        """
        self.send(f"gbconfig --network-isolation {mode}")

    def get_network_isolation_enabled(self) -> str:
        """Returns the current network isolation mode"""
        return self.send("gbconfig -s network-isolation")

    def set_network_ip_address(
        self,
        ip_type: str,
        ip_mode: str,
        ip_address: str = None,
        subnet_mask: str = None,
        gateway: str = None,
        dns_server: str = None,
    ):
        """
        Configures the IP address of the device.

        Args:
            ip_type (str): Specifies which IP address to set, either "control" or "service".
            ip_mode (str): The IP mode to use, either "dhcp" or "static".
            ip_address (str, optional): The IP address to set. Required for static IP mode. Defaults to None.
            subnet_mask (str, optional): The subnet mask. Required for static IP mode. Defaults to None.
            gateway (str, optional): The gateway IP address. Defaults to None.
            dns_server (str, optional): The DNS server IP address. Defaults to None.
        """
        command = f"gbconfig --ip-address {ip_type} {ip_mode}"
        if ip_mode == "static":
            command += f" {ip_address} {subnet_mask} {gateway} {dns_server}"
        self.send(command)

    def get_network_ip_address(self) -> list:
        """Get the IP Addresses of the device"""
        response = self.send("gbconfig -s ip-address")
        ip_info = []

        for line in response.split("\n"):
            parts = line.split()
            if len(parts) >= 2:
                info = {
                    "ethernet": parts[0],
                    "mode": parts[1],
                    "ip": parts[2] if len(parts) > 2 else "0.0.0.0",
                    "netmask": parts[3] if len(parts) > 3 else "0.0.0.0",
                    "gateway": parts[4] if len(parts) > 4 else "0.0.0.0",
                    "dns": parts[5] if len(parts) > 5 else "0.0.0.0",
                }
                ip_info.append(info)

        return ip_info

    def set_usbc_nic_enabled(self, mode: str = "y"):
        """
        Sets the USBC NIC mode
        Valid modes: y, n
        """
        self.send(f"gbconfig --nic-enable {mode}")

    def get_usbc_nic_enabled(self) -> bool:
        """Returns the current USBC NIC mode"""
        response = self.send("gbconfig -s nic-enable")
        if response == "y":
            return True
        else:
            return False

    def set_wifi_mode(self, band: str, channel: str = "auto"):
        """
        Configures the WiFi mode (band and channel) of the device.

        Args:
            band (str): The WiFi band to use. Must be either "2" (for 2.4GHz) or "5" (for 5GHz).
            channel (str, optional): The WiFi channel to use. Defaults to "auto".
                For 2.4GHz: Valid values are "1" through "11" or "auto".
                For 5GHz: Valid values are "36", "40", "44", "48", "149", "153", "157", "161", or "auto".

        Returns:
            str: The response from the device (empty string if successful).

        Raises:
            ValueError: If invalid band or channel is provided.
        """
        # Validate band
        if band not in ["2", "5"]:
            raise ValueError("Band must be either '2' (2.4GHz) or '5' (5GHz)")

        # Validate channel
        valid_channels = {
            "2": set(map(str, range(1, 12))) | {"auto"},
            "5": {"36", "40", "44", "48", "149", "153", "157", "161", "auto"},
        }
        if channel not in valid_channels[band]:
            raise ValueError(
                f"Invalid channel for {band}GHz band. Valid channels are: {', '.join(valid_channels[band])}"
            )

        # Send command
        return self.send(f"gbconfig --wifi-mode {band} {channel}")

    def get_wifi_mode(self) -> dict:
        """
        Retrieves the current WiFi mode (band and channel) of the device.

        Returns:
            dict: A dictionary containing the current WiFi band, channel, and auto status.
                Example: {"band": "5", "channel": "36", "auto": False}
                or {"band": "2", "channel": "3", "auto": True}
        """
        response = self.send("gbconfig -s wifi-mode")
        parts = response.split()
        result = {"band": "unknown", "channel": "unknown", "auto": False}

        if len(parts) >= 2:
            result["band"] = parts[0]
            if len(parts) >= 3:
                result["channel"] = parts[1]
                if parts[-1].lower() == "auto":
                    result["auto"] = True

        return result

    def set_softap_enabled(self, mode: str = "y"):
        """
        Sets the SoftAP mode
        Valid modes: y, n
        """
        self.send(f"gbconfig --softap-enable {mode}")

    def get_softap_enabled(self) -> bool:
        """Returns the current SoftAP mode"""
        response = self.send("gbconfig -s softap-enable")
        if response == "y":
            return True
        else:
            return False

    def set_softap_password(self, password: str):
        """
        Sets the password for the SoftAP
        Default password: 12345678
        """
        self.send(f"gbconfig --softap-password {password}")

    def get_softap_password(self) -> str:
        """Returns the current SoftAP password"""
        return self.send("gbconfig -s softap-password")

    def set_softap_router_enabled(self, mode: str = "y"):
        """
        Configure whether to enable the soft router. Basing on the soft AP,
        the device can launch a built in NAT module with which a device
        connected to the soft AP can access the LAN/WAN through the device's wired network interface.
        Valid modes: y, n
        """
        self.send(f"gbconfig --softap-router {mode}")

    def get_softap_router_enabled(self) -> bool:
        """Returns the current SoftAP router mode"""
        response = self.send("gbconfig -s softap-router")
        if response == "y":
            return True
        else:
            return False

    def set_byod_enabled(self, mode: str = "y"):
        """
        Configure whether to enable BYOD.
        Valid modes: y, n
        """
        self.send(f"gbconfig --byod-enable {mode}")

    def get_byod_enabled(self) -> bool:
        """Returns the current BYOD mode"""
        response = self.send("gbconfig -s byod-enable")
        if response == "y":
            return True
        else:
            return False

    def set_byod_access_code(self, access_code: str = "auto"):
        """Configure BYOD access code (PIN).
        Valid access_code: auto, none, 4 digits

        The parameter access_code consists of 4 digits.
        auto means the device automatically generates the access code and
        changes it dynamically. none means there is no access code.
        Now access code works for Airplay Mirroring and Miracast only.
        It has no use for Google Cast and Dongle."""
        self.send(f"gbconfig --access-code {access_code}")

    def get_byod_access_code(self) -> str:
        """Returns the current BYOD access code"""
        return self.send("gbconfig -s access-code")

    def get_layouts(self):
        """Returns the current layout of the device"""
        return self.send("gblayout --list")


if __name__ == "__main__":
    import time

    fsc = FSC640_Device("10.0.40.10")
    fsc.connect()
    commands = [
        fsc.get_device_info(),
        fsc.get_output_resolution(),
        fsc.get_video_output_status(),
        fsc.get_usb_host_mode(),
        fsc.get_auto_standby(),
        fsc.get_auto_standby_timeout(),
        fsc.get_cec_command(),
        fsc.get_rs232_command(),
        fsc.get_sinkpower_mode(),
        fsc.get_sinkpower(),
        fsc.get_network_ip_address(),
        fsc.get_usbc_nic_enabled(),
        fsc.get_wifi_mode(),
        fsc.get_softap_enabled(),
        fsc.get_softap_password(),
        fsc.get_softap_router_enabled(),
        fsc.get_byod_enabled(),
        fsc.get_byod_access_code(),
    ]
    for command in commands:
        command

    fsc.get_layouts()

    (fsc.start_video("hdmi", 1),)
    (fsc.start_video("usbc", 2),)
    time.sleep(5)
    fsc.stop_video()
    fsc.stop_video()
    # fsc.stop_video("hdmi")
    # fsc.stop_video("usbc")
    fsc.close()
