PROTOC = protoc
CWD := $(shell pwd)
PROTOBUF_SRC := $(CWD)/protobuf
ENTITIES_DIR := $(CWD)/entities

# Entities Protobuf definitions generation.
# Assumes that Entities Protoc-plugin is installed.
# It is located in "entities/proto/plugins/python".

# Entities: generate test entity-classes for Python.
.PHONY: entities-py-test-proto
entities-py-test-proto:
	$(PROTOC) \
		--proto_path $(PROTOBUF_SRC)/src \
		--proto_path $(ENTITIES_DIR)/proto/ \
		--proto_path $(ENTITIES_DIR)/python/ \
		--python_out $(ENTITIES_DIR)/python/ \
		--entities_out $(ENTITIES_DIR)/python/ \
		$(wildcard $(ENTITIES_DIR)/python/tests/*.proto) $(wildcard $(ENTITIES_DIR)/python/tests/**/*.proto) $(wildcard $(ENTITIES_DIR)/python/tests/**/**/*.proto)
