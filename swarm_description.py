SWARM_DESCRIPTION = {
  "includedFields": [
    {
      "fieldName": "duration",
      "fieldType": "int"
    },
    {
      "fieldName": "protocol_type",
      "fieldType": "string"
    },
    {
      "fieldName": "service",
      "fieldType": "string"
    },
    {
      "fieldName": "flag",
      "fieldType": "string"
    },
    {
      "fieldName": "src_bytes",
      "fieldType": "int"
    },
    {
      "fieldName": "dst_bytes",
      "fieldType": "int"
    },
    {
      "fieldName": "class",
      "fieldType": "string"
    }
  ],
  "streamDef": {
    "info": "kdd_cup_99",
    "version": 1,
    "streams": [
      {
        "info": "network intrusion",
        "source": "file://network_intrusion_detection.csv",
        "columns": [
          "*"
        ]
      }
    ]
  },

  "inferenceType": "TemporalMultiStep",
  "inferenceArgs": {
    "predictionSteps": [
      1
    ],
    "predictedField": "class"
  },
  "iterationCount": 5000,
  "swarmSize": "small"
}
