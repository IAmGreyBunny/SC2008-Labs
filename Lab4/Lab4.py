#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from ipwhois import IPWhois


# ## Helper Functions

# In[2]:


# Identify the organisation through IP address
ip_org_mapping = {}

def get_organisation(ip_addr):
    if ip_addr in ip_org_mapping:
        return ip_org_mapping[ip_addr]
    else:
        ip = IPWhois(ip_addr)
        result = ip.lookup_rdap()
        ip_org_mapping[ip_addr] = result.get('network', {}).get('name')
    return result.get('network', {}).get('name')

# Identify common ports
def get_service_name(port):
    port_mapping = {
        20: "FTP Data",
        21: "FTP Control",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        67: "DHCP Server",
        68: "DHCP Client",
        69: "TFTP",
        80: "HTTP",
        110: "POP3",
        123: "NTP",
        143: "IMAP",
        161: "SNMP",
        194: "IRC",
        389: "LDAP",
        443: "HTTPS",
        465: "SMTPS",
        514: "Syslog",
        515: "LPD",
        587: "SMTP (Submission)",
        636: "LDAPS",
        993: "IMAPS",
        995: "POP3S",
        1433: "MS SQL",
        1521: "Oracle",
        1723: "PPTP",
        3306: "MySQL",
        3389: "RDP",
        5060: "SIP",
        5432: "PostgreSQL",
        5900: "VNC",
        6379: "Redis",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt",
        8888: "Alternative HTTP",
        9000: "Custom/Development",
        27017: "MongoDB",
        25565: "Minecraft"
    }

    if port in port_mapping:
        return port_mapping[port]
    else:
        return "Dynamic/Unknown Port"


# ## Read in Data

# In[3]:


columns = [
    "Type",
    "sflow_agent_address",
    "inputPort",
    "outputPort",
    "src_MAC",
    "dst_MAC",
    "ethernet_type",
    "in_vlan",
    "out_vlan",
    "src_IP",
    "dst_IP",
    "IP_protocol",
    "ip_tos",
    "ip_ttl",
    "src_port",
    "dst_port",
    "tcp_flags",
    "packet_size",
    "IP_size",
    "sampling_rate"
]


# In[4]:


df = pd.read_csv("Data_2.csv",header=None,names=columns)
df = df[df["Type"]=="FLOW"] # Filter to only FLOW type
print(df.dtypes)
df.head()


# ## Top 5 Talkers

# In[5]:


top_talker = df.dropna(subset=['src_IP', 'dst_IP']) # Drop data with no src and dst ip
top_talker = top_talker['src_IP'].value_counts().head(5)

# Convert Back to dataframe
top_talker = top_talker.reset_index()
top_talker.columns = ['src_IP', 'Number of Packets'] # Rename column

# Get organisations
top_talker['organization'] = top_talker['src_IP'].apply(get_organisation)


# In[6]:


top_talker.head()


# ## Top 5 Listener

# In[7]:


top_listener = df.dropna(subset=['src_IP', 'dst_IP']) # Drop data with no src and dst ip
top_listener = top_listener['dst_IP'].value_counts().head(5)

# Convert Back to dataframe
top_listener = top_listener.reset_index()
top_listener.columns = ['dst_IP', 'Number of Packets'] # Rename column

# Get organisations
top_listener['organization'] = top_listener['dst_IP'].apply(get_organisation)


# In[8]:


top_listener.head()


# ## Top 5 Applications

# In[9]:


top_apps = df['dst_port']
top_apps = top_apps.dropna()# Drop data with no dst port
top_apps = top_apps.value_counts().head(5) 

# Convert Back to Dataframe
top_apps = top_apps.reset_index()
top_apps.columns = ['dst_port','Number of Packets']

# Get Service Name
top_apps["Service Name"] = top_apps['dst_port'].apply(get_service_name)


# In[10]:


top_apps.head()


# ## Total Traffic

# In[11]:


total_traffic = sum(df['IP_size'])
total_traffic_Mb = (total_traffic * 2048) / (1* pow(2, 20))
print(f"Total Traffic (Mb) = {total_traffic_Mb:.3f} Mb") 


# ## Proportion of TCP and UDP packets

# In[12]:


protocol_counts = df[(df['IP_protocol'] == 6) | (df['IP_protocol'] == 17)]
protocol_counts = protocol_counts['IP_protocol'].value_counts()

protocol_counts = protocol_counts.reset_index()
protocol_counts.columns = ['Protocol', 'Count']

protocol_map = {6: 'TCP', 17: 'UDP'}
protocol_counts['Protocol Name'] = protocol_counts['Protocol'].map(protocol_map)

protocol_counts.head()



# In[13]:


total_count = protocol_counts['Count'].sum()
for index, row in protocol_counts.iterrows():
    proportion = row['Count'] / total_count
    print(f"{row['Protocol Name']}: {proportion:.2%}")


# # Additional Analysis

# ## Top 5 communication pair

# In[14]:


top_communication_pair = df.dropna(subset=['src_IP', 'dst_IP']) # Drop data with no src and dst ip

# Count occurrences of each src-dst pair
top_communication_pair = (
    top_communication_pair
    .groupby(['src_IP', 'dst_IP'])
    .size()  
    .reset_index(name='Number of Packets')
    .sort_values(by='Number of Packets', ascending=False)
    .head(5)
)

top_communication_pair['From'] = top_communication_pair['src_IP'].apply(get_organisation)
top_communication_pair['To'] = top_communication_pair['dst_IP'].apply(get_organisation)

top_communication_pair = top_communication_pair.reset_index(drop=True)
top_communication_pair.head()


# ## Visualizing the communication between different IP hosts.

# In[15]:


communication_pairs = df.dropna(subset=['src_IP', 'dst_IP']) # Drop data with no src and dst ip

# Count occurrences of each src-dst pair
communication_pairs = (
    communication_pairs
    .groupby(['src_IP', 'dst_IP'])
    .size()  
    .reset_index(name='Number of Packets')
    .sort_values(by='Number of Packets', ascending=False)
    .head(20)
)



# In[16]:


communication_pairs.head()


# In[17]:


communication_pairs['From'] = communication_pairs['src_IP'].apply(get_organisation)
communication_pairs['To'] = communication_pairs['dst_IP'].apply(get_organisation)

communication_pairs = communication_pairs.reset_index(drop=True)
communication_pairs.head()


# In[18]:


import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

# Add edges
for _, row in communication_pairs.iterrows():
    src = row['From']

    dst = row['To']
    weight = row['Number of Packets']
    G.add_edge(src, dst, weight=weight)



# In[19]:


plt.figure(figsize=(10, 8))

pos = nx.shell_layout(G)

nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')

edges = G.edges(data=True)
nx.draw_networkx_edges(
    G, pos,
    edgelist=edges,
    width=[edge[2]['weight'] / 1000 for edge in edges],
    arrowstyle='->',
    arrowsize=15,
    edge_color='gray'
)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10)

plt.title("Top 20 Heaviest Connections (by number of packets)")
plt.axis('off')
plt.show()


# ### Observations from graph
# 1. The graph shows most connection are mostly unidirectional
# 2. There's no obvious central hub
# 3. The graph is very sparse with some of the connection being only between the pair
# 4. A-STAR-AS-AP is the most heavy in traffic by number of packets which can be seen by the thickness of the connection
# 5. Most of these nodes seem to belong to universities, software services as well as telcoms

# ### Insights
# The observed network is likely to be a network of research organisation since it consists mostly of universities and research organisations. The many isolated pairs and dominance of unidirectional traffic suggest the observed network connections are mostly peer to peer. Futhermore, no obvious central hub could be seen from the graph, therefore reinforcing the idea that this is a mostly peer to peer network. In a client-server network, we would expect heavy traffic on one of the nodes in terms of both number of packets as well as nuber of connections.

# ## Learnings
# 1. We can gain deeper insights into network through visualisation like network graphs
# 2. Whois lookup is slow and is a bottleneck when it comes to the analysis of the network log, most operation can be done straight from the IP address so we should only do lookups when necessary such as in the final visualisations, this can be further mitigated through caching in a dictionary map to avoid re-lookups.

# In[ ]:




