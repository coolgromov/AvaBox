import json
import binascii
import struct
import protocol
from modules.base_module import Module

class_name = "Campaign"

class Campaign(Module):
	prefix = "cm"

	def __init__(self, server):
		self.server = server
		self.commands = {}
		self.campaigns_data = None
		self.update_campaigns()
			
	def update_campaigns(self):
		baseCampaigns = []
		with open("campaigns.json", "r") as f:
			baseCampaigns = json.load(f)
		self.campaigns_data = struct.pack(">b", 34)
		self.campaigns_data += protocol.encodeArray(["cm.new", {"campaigns": baseCampaigns}])
		self.campaigns_data = self._make_header(self.campaigns_data) + self.campaigns_data
	
	def _make_header(self, msg):
		header_length = 1
		mask = 0
		mask |= (1 << 3)
		header_length += 4
		buf = struct.pack(">i", len(msg)+header_length)
		buf += struct.pack(">B", mask)
		buf += struct.pack(">I", binascii.crc32(msg))
		return buf  
		
	async def send_campaigns(self, client):
		if client.drop:
			return
		try:
			client.writer.write(self.campaigns_data)
			await client.writer.drain()
		except (BrokenPipeError, ConnectionResetError, AssertionError,
				TimeoutError, OSError, AttributeError):
			client.writer.close()