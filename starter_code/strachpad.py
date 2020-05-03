mydict = {'user': 'Bot', 'version': 0.15, 'items': 43, 'methods': 'standard', 'time': 1536304833437, 'logs': 'no', 'status': 'completed'}

columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in mydict.keys())
values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in mydict.values())
sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('mytable', columns, values)
print(sql)