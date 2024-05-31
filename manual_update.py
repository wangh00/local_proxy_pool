from merge.merge_yaml import update_agent, merge_yaml

"""
手动更新,运行这两个方法，新生成的config.yaml文件导入到v2rayN中
v2rayN中的自定义配置文件,内核选择clash-meta,端口选择一个未占用的
"""
update_agent()
merge_yaml()

